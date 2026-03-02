import torch
import sys
import os
from transformers import RobertaTokenizer
from model.train import BugPredictor

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load model
    model_path = "best_model.pt"
    if not os.path.exists(model_path):
        model_path = "last_model.pt"
    
    if not os.path.exists(model_path):
        print(f"Model not found at best_model.pt or {model_path}")
        return
        
    print(f"Loading model from {model_path}...")

    # Set weights_only=False to allow loading complex objects like optimizer state
    # This might be needed for newer PyTorch versions handling older checkpoints or complex dicts
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    # config = checkpoint['config'] # Config might be useful but redundant here
    
    model = BugPredictor(codebert_model="microsoft/codebert-base")
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    
    # Test cases from synthetic generation logic
    test_cases = [
        {
            "code": "if x = 5:\n    print('error')", 
            "expected": 1, 
            "desc": "Comparison error"
        },
        {
            "code": "if x == 5:\n    print('ok')", 
            "expected": 0, 
            "desc": "Correct comparison"
        },
        {
            "code": "while True:\n    print('loop')\n    # Missing break", 
            "expected": 1, 
            "desc": "Infinite loop"
        },
        {
            "code": "for i in range(len(arr) + 1):\n    print(arr[i])", 
            "expected": 1, 
            "desc": "Off by one"
        },
         {
            "code": "def foo(x):\n    return x + 1", 
            "expected": 0, 
            "desc": "Simple function"
        }
    ]
    
    print("\nRunning verification...")
    total = len(test_cases)
    passed = 0
    
    for case in test_cases:
        inputs = tokenizer(
            case['code'], 
            return_tensors='pt', 
            max_length=512, 
            padding='max_length', 
            truncation=True
        )
        
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        
        with torch.no_grad():
            outputs = model(input_ids, attention_mask)
            logits = outputs['logits']
            probs = torch.softmax(logits, dim=1)
            pred = torch.argmax(logits, dim=1).item()
            prob_bug = probs[0][1].item()
            
        status = "PASS" if pred == case['expected'] else "FAIL"
        if status == "PASS": passed += 1
        
        print(f"[{status}] {case['desc']}")
        print(f"  Code: {case['code']}")
        print(f"  Prediction: {pred} (Prob: {prob_bug:.4f})")
        print("-" * 30)
        
    print(f"Passed {passed}/{total} tests.")

if __name__ == "__main__":
    main()
