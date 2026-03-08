"""
Prepare training data from defects4j_all.jsonl
Samples a balanced subset, splits into train/val/test.
"""
import json
import random
import os

random.seed(42)

INPUT_FILE = "../data/defects4j_all.jsonl"
MAX_SAMPLES_PER_CLASS = 3000  # 6000 total — fits RTX 3050 memory well
MAX_CODE_LEN = 2000           # Skip very long samples
MIN_CODE_LEN = 50             # Skip too-short samples

def main():
    print("Reading defects4j dataset...")
    
    buggy = []
    clean = []
    skipped = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if i % 500000 == 0 and i > 0:
                print(f"  ...processed {i:,} lines (buggy: {len(buggy)}, clean: {len(clean)})")
            
            try:
                d = json.loads(line.strip())
                code = d.get("code", "")
                label = d.get("label")
                
                if label is None or not code:
                    skipped += 1
                    continue
                
                code_len = len(code)
                if code_len < MIN_CODE_LEN or code_len > MAX_CODE_LEN:
                    skipped += 1
                    continue
                
                if label == 1 and len(buggy) < MAX_SAMPLES_PER_CLASS * 3:
                    buggy.append({"code": code, "label": 1})
                elif label == 0 and len(clean) < MAX_SAMPLES_PER_CLASS * 3:
                    clean.append({"code": code, "label": 0})
                
                # Early stop if we have enough
                if len(buggy) >= MAX_SAMPLES_PER_CLASS * 3 and len(clean) >= MAX_SAMPLES_PER_CLASS * 3:
                    break
                    
            except (json.JSONDecodeError, KeyError):
                skipped += 1
                continue
    
    print(f"Loaded: {len(buggy)} buggy, {len(clean)} clean (skipped: {skipped})")
    
    # Subsample to balanced set
    random.shuffle(buggy)
    random.shuffle(clean)
    buggy = buggy[:MAX_SAMPLES_PER_CLASS]
    clean = clean[:MAX_SAMPLES_PER_CLASS]
    
    # Combine and shuffle
    all_data = buggy + clean
    random.shuffle(all_data)
    
    # Split: 70/15/15
    n = len(all_data)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)
    
    train = all_data[:train_end]
    val = all_data[train_end:val_end]
    test = all_data[val_end:]
    
    os.makedirs("data", exist_ok=True)
    
    for name, data in [("train", train), ("val", val), ("test", test)]:
        path = f"data/{name}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
        
        labels = [d["label"] for d in data]
        print(f"{name}: {len(data)} samples (buggy: {sum(labels)}, clean: {len(labels)-sum(labels)})")
    
    print("Done! Data ready in model/data/")

if __name__ == "__main__":
    main()
