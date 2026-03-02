
import json
import random
import os

INPUT_FILE = "data/train_balanced.jsonl"
OUTPUT_FILE = "data/train_micro.jsonl"
TARGET_SIZE = 1000 # Total samples

def main():
    input_path = INPUT_FILE
    if not os.path.exists(input_path):
        # Fallback to full train if balanced doesn't exist
        input_path = "data/train.jsonl"
        print(f"Balanced dataset not found. Using {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Reading {input_path}...")
    
    buggy = []
    clean = []
    
    with open(input_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line)
                if item['label'] == 1:
                    buggy.append(item)
                else:
                    clean.append(item)
            except:
                continue
            
            # Stop early if we have enough
            if len(buggy) > TARGET_SIZE and len(clean) > TARGET_SIZE:
                break
    
    print(f"Found {len(buggy)} buggy and {len(clean)} clean samples.")
    
    # Stratified sampling
    n_per_class = TARGET_SIZE // 2
    
    sampled_buggy = random.sample(buggy, min(len(buggy), n_per_class))
    sampled_clean = random.sample(clean, min(len(clean), n_per_class))
    
    micro_data = sampled_buggy + sampled_clean
    random.shuffle(micro_data)
    
    print(f"Writing {len(micro_data)} samples to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in micro_data:
            f.write(json.dumps(item) + "\n")
            
    print("Done!")

if __name__ == "__main__":
    main()
