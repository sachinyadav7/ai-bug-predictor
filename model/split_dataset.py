
import json
import random
import os

INPUT_FILE = "data/defects4j_all.jsonl"
TRAIN_FILE = "data/train.jsonl"
VAL_FILE = "data/val.jsonl"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    valid_lines = []
    errors = 0
    
    # Check file size to warn about memory
    file_size_gb = os.path.getsize(INPUT_FILE) / (1024**3)
    print(f"File size: {file_size_gb:.2f} GB. Loading into memory...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                valid_lines.append(obj)
            except json.JSONDecodeError:
                errors += 1
                if errors < 10:
                    print(f"Skipping invalid line {i+1}")
                elif errors == 10:
                    print("Skipping further invalid lines silently...")
    
    print(f"Loaded {len(valid_lines)} valid samples. Skipped {errors} invalid lines.")
    
    if not valid_lines:
        print("No valid data found.")
        return

    print("Shuffling...")
    random.shuffle(valid_lines)

    split_idx = int(len(valid_lines) * 0.8)
    train_data = valid_lines[:split_idx]
    val_data = valid_lines[split_idx:]

    print(f"Writing {len(train_data)} training samples to {TRAIN_FILE}...")
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    print(f"Writing {len(val_data)} validation samples to {VAL_FILE}...")
    with open(VAL_FILE, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")

    print("Done!")

if __name__ == "__main__":
    main()
