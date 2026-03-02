
import sys
import os

# Add backend to path to import ModelManager
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.model import model_manager

def test_prediction():
    print("Loading model...")
    # Ensure model is loaded (it tries to load from backend/models/bug_predictor.pt by default in ModelManager)
    # We might need to adjust the path in ModelManager or copy the file first.
    # The plan is to copy the file to backend/models/bug_predictor.pt after training.
    
    # Let's force load if it's not loaded, but ModelManager loads in __new__ or we have to call load_model manually?
    # Looking at main.py, it calls model_manager.load_model()
    
    # But wait, ModelManager hardcodes "models/bug_predictor.pt" relative to CWD?
    # In backend/app/core/model.py: load_model(self, model_path: str = "models/bug_predictor.pt")
    # If we run this from root, "models/bug_predictor.pt" might not exist if we don't copy it.
    # The training saves to "best_model.pt" in root.
    
    # So we should copy valid model to expected location before running this.
    
    # Check where the model file is
    model_path = os.path.join("backend", "models", "bug_predictor.pt")
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        # Check if we have a trained model in current directory
        if os.path.exists("best_model.pt"):
            print("Found 'best_model.pt' in current directory. using that.")
            model_path = "best_model.pt"
        elif os.path.exists("last_model.pt"):
            print("Found 'last_model.pt' in current directory. using that.")
            model_path = "last_model.pt"
        else:
            print("No model found. Please wait for training to complete.")
            return

    print(f"Attempting to load model from {model_path}...", flush=True)
    
    model_manager.load_model(model_path=model_path)
    
    if model_manager._model is None:
        print("Failed to load model. Exiting.", flush=True)
        return

    # Test cases
    buggy_code = """
    def infinite_loop():
        while True:
            print("Forever")
    """
    
    clean_code = """
    def add(a, b):
        return a + b
    """
    
    print("\nTesting Buggy Code:", flush=True)
    result_buggy = model_manager.predict(buggy_code)
    print(result_buggy, flush=True)
    
    print("\nTesting Clean Code:", flush=True)
    result_clean = model_manager.predict(clean_code)
    print(result_clean, flush=True)
    
    if result_buggy['is_buggy'] and not result_clean['is_buggy']:
        print("\nSUCCESS: Model correctly identified bug and clean code.", flush=True)
    else:
        print("\nWARNING: Model predictions might be incorrect.", flush=True)


if __name__ == "__main__":
    test_prediction()
