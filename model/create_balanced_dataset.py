
import json
import random
import os

INPUT_FILE = "data/train.jsonl"
OUTPUT_FILE = "data/train_balanced.jsonl"
TARGET_SIZE = 25000 # Total samples

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    
    buggy = []
    clean = []
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line)
                if item['label'] == 1:
                    buggy.append(item)
                else:
                    clean.append(item)
            except:
                continue
            
            # Optimization: Stop reading if we have enough of both
            # But we want a good distribution, so maybe read all? 
            # 6M lines is a lot. Let's read first 500k to get a good sample.
            if i > 500000 and len(buggy) > TARGET_SIZE and len(clean) > TARGET_SIZE:
                break
    
    print(f"Found {len(buggy)} buggy and {len(clean)} clean samples (scanned {i} lines).")
    
    # Stratified sampling
    n_per_class = TARGET_SIZE // 2
    
    sampled_buggy = random.sample(buggy, min(len(buggy), n_per_class))
    sampled_clean = random.sample(clean, min(len(clean), n_per_class))
    
    balanced_data = sampled_buggy + sampled_clean
    random.shuffle(balanced_data)
    
    print(f"Writing {len(balanced_data)} samples to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in balanced_data:
            f.write(json.dumps(item) + "\n")
            
    print("Done!")

if __name__ == "__main__":
    main()
