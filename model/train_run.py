from train import BugPredictionTrainer, CONFIG
from dataset import build_loaders
import os
import torch
import sys

def main():
    print("Starting training run...")
    
    # Update config for faster training on CPU
    # Update config for real data training
    # Update config for real data training - OPTIMIZED FOR NANO / SPEED
    CONFIG['max_length'] = 512 
    CONFIG['epochs'] = 1
    CONFIG['learning_rate'] = 5e-5 
    CONFIG['batch_size'] = 8
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data/ directory.")
    
    # check for nano dataset first
    train_file = "data/train_nano.jsonl"
    if not os.path.exists(train_file):
        print(f"Nano dataset {train_file} not found. Checking micro...")
        train_file = "data/train_micro.jsonl"
    
    if not os.path.exists(train_file):
         print(f"Micro dataset {train_file} not found. Falling back to full train.jsonl")
         train_file = "data/train.jsonl"
    else:
        print(f"Using dataset: {train_file}")

    if not os.path.exists(train_file):
        print("Error: Training data not found.")
        return
        
    train_loader, val_loader = build_loaders(
        train_path=train_file,
        val_path="data/val.jsonl", 
        batch_size=CONFIG.get('batch_size', 8),
        max_length=CONFIG.get('max_length', 128)
    )

    if len(train_loader.dataset) == 0:
        print("Aborting training due to empty dataset.")
        return

    trainer = BugPredictionTrainer(CONFIG)
    
    print(f"Training on {len(train_loader.dataset)} samples")
    history = trainer.train(train_loader, val_loader, epochs=CONFIG.get('epochs', 5))
    
    # Final save (best model is already saved by early stopping)
    # But let's ensure we save the last state too if needed, 
    # though best_model.pt is what we want.
    
    print("Training complete.")

if __name__ == "__main__":
    main()
