import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path so we can import backend.app.core.model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Also add root for model.train import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

class TestModelFixes(unittest.TestCase):
    
    def setUp(self):
        # Clear singleton if it exists
        if 'backend.app.core.model' in sys.modules:
            del sys.modules['backend.app.core.model']
            
    def test_model_missing_behavior(self):
        """Test that missing model file triggers checking logic (prints error, no random weights)"""
        
        # Mock os.path.exists to return False for model path
        with patch('os.path.exists', return_value=False):
            from backend.app.core.model import model_manager
            
            # Check initialized state
            self.assertIsNone(model_manager._model, "Model should be None if file missing")
            self.assertEqual(model_manager._threshold, 0.5, "Threshold should default to 0.5")
            
            # Predict request should return error or specific fallback
            model_manager._tokenizer = MagicMock() # Mock tokenizer
            
            # Mock heuristics to return None
            with patch.object(model_manager, '_check_heuristics', return_value=None):
                result = model_manager.predict("print('hello')")
                print(f"Prediction result when model missing: {result}")
                self.assertFalse(result['is_buggy'])
                self.assertEqual(result['confidence'], 0.0)
                self.assertIn('error', result)
                self.assertEqual(result['error'], "Model not loaded")

    def test_heuristics_combination(self):
        """Test that heuristics are combined with ML results"""
        with patch('os.path.exists', return_value=True):
            with patch('torch.load') as mock_load:
                mock_load.return_value = {
                    'model_state_dict': {},
                    'threshold': 0.6
                }
                
                # Mock BugPredictor to avoid needing actual model structure
                with patch('backend.app.core.model.BugPredictor') as MockBugPredictor:
                    mock_model_instance = MockBugPredictor.return_value
                    # Mock forward pass
                    mock_model_instance.return_value = {'logits': MagicMock()} 
                    # We need to mock torch.sigmoid or the output of the model
                    # But since we are mocking the whole model call in predict, let's mock torch.sigmoid
                    
                    from backend.app.core.model import model_manager
                    
                    # Verify threshold loaded
                    self.assertEqual(model_manager._threshold, 0.6)
                    
                    # Mock _check_heuristics to return a high confidence bug
                    heuristic_res = {
                        'is_buggy': True, 
                        'confidence': 0.9, 
                        'risk_level': 'high',
                        'highlighted_tokens': [{'token': 'BUG'}]
                    }
                    
                    # Mock ML prediction to be low confidence (0.1)
                    # We have to be careful as predict() calls _check_heuristics internally
                    # We'll partial mock it
                    
                    with patch.object(model_manager, '_check_heuristics', return_value=heuristic_res) as mock_heuristics:
                         # IMPORTANT: logic says if heuristics, return heuristics immediately?
                         # NO, we changed it to combine!
                         # Wait, check my edit.
                         # "3. Combine Results" code block
                         # BUT "1. Heuristic Check" block says:
                         # "if self._model is None: if heuristic_result: return heuristic_result"
                         # Main path: it calls heuristics, then ML, then combines.
                         
                         # Wait, the logic I wrote:
                         # heuristic_result = self._check_heuristics(code)
                         # ... ML prediction ...
                         # Combine
                         
                         # BUT wait, did I remove the early return?
                         # "heuristic_result = self._check_heuristics(code)
                         #  [DELETED] if heuristic_result: return heuristic_result "
                         # Yes, I removed it in my edit.
                         
                         # So it should run ML.
                         
                         # We need to mock ML part to return something valid
                         # Mock torch.sigmoid
                         with patch('torch.sigmoid') as mock_sigmoid:
                             # Return tensor with 0.2
                             mock_tensor = MagicMock()
                             mock_tensor.__getitem__.return_value.item.return_value = 0.2
                             mock_sigmoid.return_value = MagicMock()
                             mock_sigmoid.return_value.__getitem__.return_value = mock_tensor
                             
                             # Mock tokenizer
                             model_manager._tokenizer = MagicMock()
                             model_manager._tokenizer.return_value.to.return_value = {
                                 'input_ids': MagicMock(),
                                 'attention_mask': MagicMock()
                             }
                             # Mock attention mask sum
                             model_manager._tokenizer.return_value.to.return_value['attention_mask'].sum.return_value.item.return_value = 10

                             result = model_manager.predict("some code")
                             
                             # ML gave 0.2, Heuristics gave 0.9. Result confidence should be 0.9
                             self.assertEqual(result['confidence'], 0.9)
                             self.assertTrue(result['is_buggy'])
                             self.assertEqual(result['risk_level'], 'high')

if __name__ == '__main__':
    unittest.main()
