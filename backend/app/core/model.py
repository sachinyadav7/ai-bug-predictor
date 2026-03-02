import torch
import os
from typing import Dict, List, Tuple, Optional
from transformers import RobertaTokenizer
import sys
# Assuming we run from backend/ directory, '..' puts us in project root where 'model' package is.
sys.path.append('..')
try:
    from model.train import BugPredictor  # Import from training code
except ImportError:
    # Fallback if running from root
    from model.train import BugPredictor

class ModelManager:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: str = "models/bug_predictor.pt"):
        """Load model once at startup"""
        if self._model is not None:
            return
        
        self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize model architecture
        self._model = BugPredictor()
        
        # Load weights
        # Load weights
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path, map_location=self._device, weights_only=False)
            self._model.load_state_dict(checkpoint['model_state_dict'])
            # Load threshold if available, else default to 0.5
            self._threshold = checkpoint.get('threshold', 0.5)
            print(f"Model loaded with threshold: {self._threshold}")
        else:
            # STOP! Do not use random weights.
            print(f"CRITICAL ERROR: Model checkpoint not found at {model_path}.")
            print("Cannot run predictions with random weights.")
            self._threshold = 0.5
            # We don't raise exception here to avoid crashing server on import, 
            # but predict() should fail or handle this.
            self._model = None
            return

        self._model.to(self._device)
        self._model.eval()
        
        self._tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        
        print(f"Model loaded on {self._device}")
    
    def predict(self, code: str) -> Dict:
        """Single prediction"""
        
        # 1. Heuristic Check (Rule-Based Fallback)
        heuristic_result = self._check_heuristics(code)
        
        # 2. ML Prediction
        # If model is not loaded (missing checkpoint), fallback to heuristics only or error
        if self._model is None:
            if heuristic_result:
                return heuristic_result
            return {
                'is_buggy': False,
                'confidence': 0.0,
                'risk_level': "low",
                'error': "Model not loaded"
            }

        # Preprocess
        inputs = self._tokenizer(
            code,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding='max_length'
        ).to(self._device)
        
        with torch.no_grad():
            outputs = self._model(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask']
            )
        
        # USE SIGMOID for binary classification
        # outputs['logits'] shape: [1, 2] -> we want prob of class 1 (buggy)
        # But wait, original code used 2 logits. 
        # If we use sigmoid on logits[:, 1], it assumes logit 1 is 'buggy' score vs independent logit 0.
        # Standard approach with 2 output neurons: softmax.
        # User explicitly requested: "bug_prob = torch.sigmoid(outputs['logits'][:,1])[0].item()"
        # This implies checking the absolute activation of the 'buggy' node.
        
        bug_prob = torch.sigmoid(outputs['logits'][:,1])[0].item()
        
        ml_result = {
            'is_buggy': bug_prob > self._threshold,
            'confidence': bug_prob,
            'risk_level': self._get_risk_level(bug_prob),
            'tokens_analyzed': inputs['attention_mask'].sum().item()
        }

        # 3. Combine Results
        if heuristic_result:
            # If heuristic detected something high confidence, push up the confidence
            ml_result['confidence'] = max(ml_result['confidence'], heuristic_result['confidence'])
            
            # If heuristic says buggy (high conf), override is_buggy to True
            if heuristic_result['is_buggy']:
                ml_result['is_buggy'] = True
                ml_result['risk_level'] = "high" # Force high risk for regex matches like 'password='
                
            # Merge highlighted tokens if we had them in ML result (we don't currently, but for future)
            if 'highlighted_tokens' in heuristic_result:
                ml_result['highlighted_tokens'] = heuristic_result['highlighted_tokens']

        return ml_result
        
    def _check_heuristics(self, code: str) -> Optional[Dict]:
        """Detect common bug patterns using regex/string matching"""
        import re
        
        patterns = [
            # Python
            (r'while\s+True\s*:', 'Potential Infinite Loop (Python)', 0.95),
            (r'/\s*0', 'Division by Zero', 0.99),
            (r'except\s*:', 'Broad Exception Handler (Python)', 0.85),
            (r'eval\s*\(', 'Dangerous Use of eval()', 0.90),
            (r'exec\s*\(', 'Dangerous Use of exec()', 0.90),
            
            # Java / General
            (r'while\s*\(\s*true\s*\)', 'Potential Infinite Loop (Java/C)', 0.95),
            (r'catch\s*\(\s*Exception\s+\w+\s*\)\s*\{\s*\}', 'Empty Catch Block (Java)', 0.90),
            (r'\bnull\b', 'Potential Null Reference Risk', 0.75),
            (r'System\.out\.println', 'Leftover Debug Print', 0.40), # Low risk, but annoying
            
            # Security / Secrets
            (r'password\s*=\s*[\'"].+[\'"]', 'Hardcoded Password', 0.92),
            (r'token\s*=\s*[\'"].+[\'"]', 'Hardcoded API Token', 0.92),
            
            # User Annotations (The user knows best!)
            (r'//\s*BUG', 'Explicit Bug Annotation', 1.0),
            (r'//\s*FIXME', 'FIXME Annotation', 0.80),
            (r'TODO:', 'Pending TODO', 0.30),
        ]
        
        risk_tokens = []
        max_conf = 0
        
        for pattern, name, conf in patterns:
            # Case insensitive for some? No, code is case sensitive usually.
            if re.search(pattern, code):
                max_conf = max(max_conf, conf)
                risk_tokens.append({'token': name})
                
        if max_conf > 0.4: # Only return if confidence is significant
            return {
                'is_buggy': max_conf > 0.5,
                'confidence': max_conf,
                'risk_level': self._get_risk_level(max_conf),
                'highlighted_tokens': risk_tokens,
                'tokens_analyzed': len(code.split())
            }
            
        return None
    
    def predict_batch(self, codes: List[str]) -> List[Dict]:
        """Batch prediction for efficiency"""
        inputs = self._tokenizer(
            codes,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        ).to(self._device)
        
        with torch.no_grad():
            outputs = self._model(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask']
            )
        
        return results
    
    def _get_risk_level(self, prob: float) -> str:
        if prob < 0.3:
            return "low"
        elif prob < 0.7:
            return "medium"
        return "high"

# Singleton instance
model_manager = ModelManager()
