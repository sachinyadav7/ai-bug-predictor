from transformers import RobertaTokenizer
import torch
# from datasets import Dataset # Commented out as we might not need 'datasets' library immediately for inference, but keeping request txt has it.

class CodeTokenizer:
    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        self.max_length = 512
    
    def tokenize_function(self, examples):
        """Tokenize code for CodeBERT"""
        # Tokenize buggy code
        tokenized = self.tokenizer(
            examples['buggy_code'],
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': tokenized['input_ids'],
            'attention_mask': tokenized['attention_mask'],
            'labels': torch.tensor(examples['label'])
        }
    
    def prepare_dataset(self, df):
        """Convert DataFrame to HuggingFace Dataset"""
        from datasets import Dataset # Import here to avoid hard dependency if not used
        dataset = Dataset.from_pandas(df)
        tokenized = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        return tokenized
