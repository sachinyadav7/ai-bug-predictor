import torch
import matplotlib.pyplot as plt
import numpy as np

class AttentionVisualizer:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def get_attention_maps(self, code):
        """Extract attention weights from all layers"""
        inputs = self.tokenizer(
            code,
            return_tensors='pt',
            truncation=True,
            max_length=512
        )
        
        # Move inputs to same device as model
        device = next(self.model.codebert.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.codebert(
                **inputs,
                output_attentions=True
            )
        
        # outputs.attentions is a tuple of 12 layers
        # Each layer: [batch, heads, seq_len, seq_len]
        attentions = torch.stack(outputs.attentions)  # [12, 1, 12, seq, seq]
        return attentions.squeeze(1), inputs['input_ids'][0]
    
    def visualize_token_importance(self, code, save_path=None):
        """Aggregate attention to show token importance"""
        attentions, input_ids = self.get_attention_maps(code)
        
        # Average across layers and heads
        # attentions shape: [layers, heads, seq, seq]
        # We want to see which tokens attended to [CLS] or generally high activation?
        # Usually we look at the attention weights of [CLS] token to other tokens (index 0)
        # Or average attention to each token from all other tokens.
        # The plan says: "Average across layers and heads" -> [seq, seq]
        # Then "Get importance (attention received by each token)" -> sum(dim=0)
        
        avg_attention = attentions.mean(dim=[0, 1])  # [seq, seq]
        
        # Get importance (attention received by each token)
        # Summing over dim=0 means summing the attention *received* by a token from all others.
        importance = avg_attention.sum(dim=0).cpu().numpy()
        
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        
        # Plot
        # We can skip plotting if no save path, just return data
        if save_path:
            plt.figure(figsize=(12, 6))
            x_pos = np.arange(len(tokens))
            plt.bar(x_pos, importance)
            plt.xticks(x_pos, tokens, rotation=90, fontsize=8)
            plt.ylabel('Attention Score')
            plt.title('Token Importance for Bug Prediction')
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
        
        return {
            'tokens': tokens,
            'importance': importance.tolist()
        }
    
    def highlight_buggy_tokens(self, code, threshold=0.5):
        """Return code with highlighted regions"""
        importance_data = self.visualize_token_importance(code)
        
        # Find high-attention spans
        tokens = importance_data['tokens']
        importance = np.array(importance_data['importance'])
        
        # Normalize
        if importance.max() > importance.min():
            importance = (importance - importance.min()) / (importance.max() - importance.min())
        else:
            importance = np.zeros_like(importance)
        
        # Group consecutive tokens
        spans = []
        current_span = []
        
        for i, (token, imp) in enumerate(zip(tokens, importance)):
            if imp > threshold:
                current_span.append({'token': token, 'importance': imp, 'index': i})
            else:
                if current_span:
                    spans.extend(current_span) # Just flatten to list of tokens for now or keep structure
                    current_span = []
        
        if current_span:
            spans.extend(current_span)
        
        return spans
