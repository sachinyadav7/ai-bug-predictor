import json
import os
from pathlib import Path

# ==========================================
# CUSTOM DATA PREPARATION SCRIPT
# ==========================================
# Usage:
# 1. Edit the `my_data` list below with your own examples.
# 2. Run this script: python preprocessing/prepare_custom_data.py
# 3. Training data will be generated in data/train.jsonl and data/val.jsonl
# ==========================================

# 1. Define your data here
# Format: {"code": "your code string", "label": 1 (buggy) or 0 (clean)}
my_data = [
    # Example 1: Buggy
    {
        "code": """def calculate_sum(arr):
    total = 0
    # Off-by-one error potential if not careful, but this is just an example
    for i in range(len(arr) + 1): 
        total += arr[i]
    return total""",
        "label": 1
    },
    # Example 2: Clean
    {
        "code": """def calculate_sum(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total""",
        "label": 0
    },
    # Add more of your own data here...
]

def main():
    if not my_data:
        print("Error: my_data list is empty. Please add your data to the script.")
        return

    # 2. Split into train/validation (80/20 split)
    # Shuffle first if needed
    # import random
    # random.shuffle(my_data)
    
    split_idx = int(len(my_data) * 0.8)
    train_data = my_data[:split_idx]
    val_data = my_data[split_idx:]
    
    # 3. Save to data/ directory (relative to project root if run from root, or relative to script)
    # Let's assume we run from project root, so 'data/' is distinct from 'preprocessing/'
    
    # Determine project root (assuming this script is in preprocessing/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    
    data_dir.mkdir(exist_ok=True)
    
    train_path = data_dir / "train.jsonl"
    val_path = data_dir / "val.jsonl"

    print(f"Writing {len(train_data)} training samples to {train_path}...")
    with open(train_path, "w", encoding='utf-8') as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    print(f"Writing {len(val_data)} validation samples to {val_path}...")
    with open(val_path, "w", encoding='utf-8') as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")

    print("\nSuccess! Data is ready.")
    print(f"To train the model, run: python model/train_run.py")

if __name__ == "__main__":
    main()
