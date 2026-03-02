
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import (
    RobertaModel,
    RobertaConfig,
    get_linear_schedule_with_warmup,
    RobertaTokenizer
)
from torch.optim import AdamW
from sklearn.metrics import f1_score, precision_recall_fscore_support
import numpy as np
from tqdm import tqdm
import os
import json

class BugPredictor(nn.Module):
    def __init__(self, codebert_model="microsoft/codebert-base", num_labels=2):
        super().__init__()
        # Retry logic for model downloading
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.codebert = RobertaModel.from_pretrained(codebert_model)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Model download failed (attempt {attempt+1}/{max_retries}). Retrying in 2s...")
                import time
                time.sleep(2)
        self.dropout = nn.Dropout(0.1)
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(self.codebert.config.hidden_size, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, num_labels)
        )
        
        # Initialize weights
        self._init_weights(self.classifier)
    
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=0.02)
            if module.bias is not None:
                module.bias.data.zero_()
    
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.codebert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        
        loss = None
        if labels is not None:
            # Weight buggy class (label 1) higher to handle imbalance
            # Suggested weight: 3.0
            weights = torch.tensor([1.0, 3.0]).to(self.classifier[0].weight.device)
            loss_fct = nn.CrossEntropyLoss(weight=weights)
            loss = loss_fct(logits, labels)
        
        return {
            'loss': loss,
            'logits': logits,
            'hidden_states': outputs.last_hidden_state,
            'attentions': outputs.attentions
        }

class BugPredictionTrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.model = BugPredictor().to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        
        # Optimizer with weight decay
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {
                'params': [p for n, p in self.model.named_parameters() 
                          if not any(nd in n for nd in no_decay)],
                'weight_decay': 0.01
            },
            {
                'params': [p for n, p in self.model.named_parameters() 
                          if any(nd in n for nd in no_decay)],
                'weight_decay': 0.0
            }
        ]
        
        self.optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=config['learning_rate'],
            eps=1e-8
        )
        
        self.best_f1 = 0
        self.patience_counter = 0
        
    def train_epoch(self, dataloader, scheduler):
        self.model.train()
        total_loss = 0
        
        progress_bar = tqdm(dataloader, desc="Training")
        for batch in progress_bar:
            # Move to device
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            self.optimizer.zero_grad()
            
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs['loss']
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            
            self.optimizer.step()
            scheduler.step()
            
            total_loss += loss.item()
            progress_bar.set_postfix({'loss': loss.item()})
        
        return total_loss / len(dataloader)
    
    def evaluate(self, dataloader):
        self.model.eval()
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Evaluating"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                
                logits = outputs['logits']
                probs = torch.sigmoid(logits[:, 1])
                all_probs.extend(probs)
                preds = torch.argmax(logits, dim=1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                 # Prob of buggy class
        
        # Metrics
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='binary'
        )
        
        # Find optimal threshold
        from sklearn.metrics import precision_recall_curve
        # Move all_probs to cpu if it's a tensor list or contains tensors
        if isinstance(all_probs, list) and len(all_probs) > 0 and isinstance(all_probs[0], torch.Tensor):
            all_probs_np = torch.stack(all_probs).cpu().numpy()
        elif isinstance(all_probs, torch.Tensor):
            all_probs_np = all_probs.cpu().numpy()
        else:
            all_probs_np = np.array(all_probs)
            
        precisions, recalls, thresholds = precision_recall_curve(all_labels, all_probs_np)
        if len(precisions) > 1:
            f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
            best_threshold = thresholds[np.argmax(f1_scores)]
        else:
            best_threshold = 0.5
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'threshold': best_threshold,
            'predictions': all_preds,
            'probabilities': all_probs
        }
    
    def train(self, train_loader, val_loader, epochs=10):
        total_steps = len(train_loader) * epochs
        scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=0.1 * total_steps,
            num_training_steps=total_steps
        )
        
        history = []
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            train_loss = self.train_epoch(train_loader, scheduler)
            val_metrics = self.evaluate(val_loader)
            
        
            
            print(f"Train Loss: {train_loss:.4f}")
            print(f"Val Precision: {val_metrics['precision']:.4f}")
            print(f"Val Recall: {val_metrics['recall']:.4f}")
            print(f"Val F1: {val_metrics['f1']:.4f}")
            print(f"Optimal Threshold: {val_metrics['threshold']:.4f}")
            
            history.append({
                'epoch': epoch,
                'train_loss': train_loss,
                **val_metrics
            })
            
            # Always save latest model
            self.save_checkpoint('last_model.pt', val_metrics)
            
            # Early stopping
            if val_metrics['f1'] > self.best_f1:
                self.best_f1 = val_metrics['f1']
                self.save_checkpoint('best_model.pt', val_metrics)
                self.patience_counter = 0
            else:
                self.patience_counter += 1
                if self.patience_counter >= 3:
                    print("Early stopping triggered")
                    break
        
        # Save history
        with open('training_history.json', 'w') as f:
            json.dump(history, f, indent=2)
        
        return history
    
    def save_checkpoint(self, path, metrics):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': metrics,
            'threshold': metrics.get('threshold', 0.5), # Save explicitly for easy loading
            'config': self.config
        }, path)
        print(f"Saved best model to {path}")

# Training configuration
CONFIG = {
    'batch_size': 16,
    'learning_rate': 2e-5,
    'epochs': 5,
    'max_length': 512,
    'weight_decay': 0.01
}

# Usage
if __name__ == "__main__":
    from dataset import build_loaders
    
    # Ensure data directory exists or use default
    if not os.path.exists("data/train.jsonl"):
        print("Error: data/train.jsonl not found. Run preprocessing/generate_synthetic_data.py first.")
        exit(1)
        
    print("Loading data...")
    train_loader, val_loader = build_loaders(
        train_path="data/train.jsonl",
        val_path="data/val.jsonl",
        batch_size=CONFIG['batch_size'],
        max_length=CONFIG['max_length']
    )
    
    print("Initializing trainer...")
    trainer = BugPredictionTrainer(CONFIG)
    
    print("Starting training...")
    history = trainer.train(train_loader, val_loader, epochs=CONFIG['epochs'])
    
    print("Training complete! Best model saved to 'best_model.pt'")
