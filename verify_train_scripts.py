import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Importing model.train...")
    from model.train import BugPredictionTrainer, CONFIG
    print("SUCCESS: model.train imported.")
except ImportError as e:
    print(f"FAILED: Could not import model.train: {e}")
    sys.exit(1)

try:
    print("Importing model.dataset...")
    from model.dataset import build_loaders, BugDataset
    print("SUCCESS: model.dataset imported.")
except ImportError as e:
    print(f"FAILED: Could not import model.dataset: {e}")
    sys.exit(1)

try:
    print("Importing model.train_run...")
    import model.train_run
    print("SUCCESS: model.train_run imported.")
except ImportError as e:
    print(f"FAILED: Could not import model.train_run: {e}")
    # train_run might fail if it tries to run main() - but it shouldn't if guarded by if __name__ == "__main__"
    sys.exit(1)

print("All training scripts verified structurally.")
