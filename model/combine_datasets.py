"""
Combine generated dataset + defects4j subset for optimal training.
The generated data has clear bug signals; defects4j adds real-world diversity.
"""
import json
import random
import os

random.seed(42)

def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                d = json.loads(line.strip())
                if 'code' in d and 'label' in d:
                    data.append({"code": d["code"], "label": int(d["label"])})
            except:
                continue
    return data

def main():
    # 1. Load our generated real-world dataset
    print("Loading generated data...")
    gen_train = load_jsonl("data/train.jsonl")
    gen_val = load_jsonl("data/val.jsonl")
    
    print(f"  Generated train: {len(gen_train)}")
    print(f"  Generated val: {len(gen_val)}")
    
    # 2. Load defects4j samples (filter for reasonable length)
    print("Loading defects4j subset...")
    d4j_buggy = []
    d4j_clean = []
    MAX_PER_CLASS = 1000  # Add 1K from each class from defects4j
    
    with open("../data/defects4j_all.jsonl", "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if len(d4j_buggy) >= MAX_PER_CLASS and len(d4j_clean) >= MAX_PER_CLASS:
                break
            try:
                d = json.loads(line.strip())
                code = d.get("code", "")
                label = int(d.get("label", -1))
                
                # Filter: 50-1500 chars (skip huge license-heavy files & tiny snippets) 
                if len(code) < 50 or len(code) > 1500:
                    continue
                
                if label == 1 and len(d4j_buggy) < MAX_PER_CLASS:
                    d4j_buggy.append({"code": code, "label": 1})
                elif label == 0 and len(d4j_clean) < MAX_PER_CLASS:
                    d4j_clean.append({"code": code, "label": 0})
            except:
                continue
    
    random.shuffle(d4j_buggy)
    random.shuffle(d4j_clean)
    
    d4j_all = d4j_buggy + d4j_clean
    random.shuffle(d4j_all)
    
    # Split defects4j: 85% train, 15% val
    d4j_split = int(len(d4j_all) * 0.85)
    d4j_train = d4j_all[:d4j_split]
    d4j_val = d4j_all[d4j_split:]
    
    print(f"  Defects4j train: {len(d4j_train)} (buggy: {sum(1 for x in d4j_train if x['label']==1)})")
    print(f"  Defects4j val: {len(d4j_val)}")
    
    # 3. Combine
    combined_train = gen_train + d4j_train
    combined_val = gen_val + d4j_val
    
    random.shuffle(combined_train)
    random.shuffle(combined_val)
    
    # Stats
    train_buggy = sum(1 for x in combined_train if x['label'] == 1)
    train_clean = len(combined_train) - train_buggy
    val_buggy = sum(1 for x in combined_val if x['label'] == 1)
    val_clean = len(combined_val) - val_buggy
    
    print(f"\nCombined train: {len(combined_train)} (buggy: {train_buggy}, clean: {train_clean})")
    print(f"Combined val: {len(combined_val)} (buggy: {val_buggy}, clean: {val_clean})")
    
    # 4. Write
    os.makedirs("data", exist_ok=True)
    
    with open("data/train.jsonl", "w", encoding="utf-8") as f:
        for item in combined_train:
            f.write(json.dumps(item) + "\n")
    
    with open("data/val.jsonl", "w", encoding="utf-8") as f:
        for item in combined_val:
            f.write(json.dumps(item) + "\n")
    
    print("Done! Combined dataset saved to data/train.jsonl and data/val.jsonl")

if __name__ == "__main__":
    main()
