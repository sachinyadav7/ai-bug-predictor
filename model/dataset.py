import torch
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaTokenizer
import json
import os
from typing import List, Tuple

class BugDataset(Dataset):
    def __init__(self, data_path: str, tokenizer, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data = []
        
        # Load JSONL data
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        else:
            print(f"Warning: Data file {data_path} not found. Creating empty dataset.")
            
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        code = item['code']
        label = int(item['label'])
        
        encoding = self.tokenizer(
            code,
            return_tensors='pt',
            max_length=self.max_length,
            padding='max_length',
            truncation=True
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def build_loaders(
    train_path: str = "data/train.jsonl",
    val_path: str = "data/val.jsonl", 
    batch_size: int = 16,
    max_length: int = 512
) -> Tuple[DataLoader, DataLoader]:
    
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    
    train_dataset = BugDataset(train_path, tokenizer, max_length=max_length)
    val_dataset = BugDataset(val_path, tokenizer, max_length=max_length)
    
    # Check if empty
    if len(train_dataset) == 0:
        print("CRITICAL: Train dataset is empty!")
    if len(val_dataset) == 0:
        print("Warning: Val dataset is empty!")

    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True,
        num_workers=0 # Avoid Windows multiprocessing issues
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=batch_size, 
        shuffle=False,
        num_workers=0
    )
    
    return train_loader, val_loader
