import json
import random
import os
from pathlib import Path

def generate_off_by_one():
    """Generates off-by-one errors in loops"""
    template_buggy = [
        "for i in range(len(arr) + 1):", 
        "    print(arr[i])",
    ]
    template_clean = [
        "for i in range(len(arr)):",
        "    print(arr[i])",
    ]
    return "\n".join(template_buggy), "\n".join(template_clean)

def generate_infinite_loop():
    """Generates infinite loops"""
    template_buggy = [
        "while True:",
        "    print('working')",
        "    # Missing break",
    ]
    template_clean = [
        "while True:",
        "    print('working')",
        "    if condition:",
        "        break",
    ]
    return "\n".join(template_buggy), "\n".join(template_clean)

def generate_comparison_error():
    """Generates comparison errors (== vs =)"""
    template_buggy = [
        "if x = 5:",
        "    print('equal')",
    ]
    template_clean = [
        "if x == 5:",
        "    print('equal')",
    ]
    return "\n".join(template_buggy), "\n".join(template_clean)

def generate_missing_return():
    """Generates missing return statements"""
    template_buggy = [
        "def calculate(a, b):",
        "    result = a + b",
        "    # Missing return",
    ]
    template_clean = [
        "def calculate(a, b):",
        "    result = a + b",
        "    return result",
    ]
    return "\n".join(template_buggy), "\n".join(template_clean)

def generate_dataset(num_samples=200, output_dir="data"):
    data = []
    generators = [
        generate_off_by_one,
        generate_infinite_loop,
        generate_comparison_error,
        generate_missing_return
    ]
    
    for _ in range(num_samples):
        gen = random.choice(generators)
        buggy, clean = gen()
        
        # Add buggy sample
        data.append({
            "code": buggy,
            "label": 1
        })
        
        # Add clean sample
        data.append({
            "code": clean,
            "label": 0
        })
        
    # Shuffle
    random.shuffle(data)
    
    # Split
    split_idx = int(len(data) * 0.8)
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    # Ensure directory exists
    Path(output_dir).mkdir(exist_ok=True)
    
    # Write files
    with open(f"{output_dir}/train.jsonl", "w") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")
            
    with open(f"{output_dir}/val.jsonl", "w") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")
            
    print(f"Generated {len(train_data)} training samples and {len(val_data)} validation samples.")

if __name__ == "__main__":
    generate_dataset()
