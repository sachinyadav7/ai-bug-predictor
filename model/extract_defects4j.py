import os
import json
import subprocess
from pathlib import Path

DEFECTS4J = "/home/sachin/defects4j"
TMP = "data/tmp"
OUT = "data/defects4j_all.jsonl"

projects = ["Lang", "Math", "Time", "Chart", "Closure"]

def run(cmd):
    subprocess.run(cmd, shell=True, check=False)

def get_java_files(folder):
    files = []
    for root, _, fs in os.walk(folder):
        for f in fs:
            if f.endswith(".java"):
                files.append(os.path.join(root, f))
    return files

def split_methods(code):
    parts = code.split("}")
    return [p + "}" for p in parts if len(p) > 80]

os.makedirs(TMP, exist_ok=True)
out = open(OUT, "w", encoding="utf-8")

for project in projects:
    print(f"\nProcessing {project}")

    for bug in range(1, 200):
        buggy_dir = f"{TMP}/{project}_{bug}b"
        fixed_dir = f"{TMP}/{project}_{bug}f"

        run(f"{DEFECTS4J}/framework/bin/defects4j checkout -p {project} -v {bug}b -w {buggy_dir}")
        run(f"{DEFECTS4J}/framework/bin/defects4j checkout -p {project} -v {bug}f -w {fixed_dir}")

        if not os.path.exists(buggy_dir):
            print(f"Skipping {project}-{bug} (not found/deprecated)")
            # Don't break immediately, some IDs might be deprecated (gaps)
            # BUT, we don't want to run until 200 if the project only has 20 bugs.
            # Strategy: if we hit 5 consecutive misses, then break.
            consecutive_misses = consecutive_misses + 1 if 'consecutive_misses' in locals() else 1
            if consecutive_misses >= 5:
                print(f"Stopping {project} after 5 consecutive misses.")
                break
            continue
        
        consecutive_misses = 0

        # BUGGY
        for f in get_java_files(buggy_dir):
            code = open(f, errors="ignore").read()
            for chunk in split_methods(code):
                out.write(json.dumps({"code": chunk, "label": 1}) + "\n")

        # FIXED
        for f in get_java_files(fixed_dir):
            code = open(f, errors="ignore").read()
            for chunk in split_methods(code):
                out.write(json.dumps({"code": chunk, "label": 0}) + "\n")

import random

print("Dataset extraction complete. Splitting into Train/Val...")
out.close()

# Read back, shuffle, and split
with open(OUT, "r", encoding="utf-8") as f:
with open(OUT, "r", encoding="utf-8") as f:
    all_data = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            all_data.append(json.loads(line))
        except json.JSONDecodeError:
            continue

random.shuffle(all_data)

split_idx = int(len(all_data) * 0.8)
train_data = all_data[:split_idx]
val_data = all_data[split_idx:]

with open("data/train.jsonl", "w", encoding="utf-8") as f:
    for item in train_data:
        f.write(json.dumps(item) + "\n")

with open("data/val.jsonl", "w", encoding="utf-8") as f:
    for item in val_data:
        f.write(json.dumps(item) + "\n")

print(f"Data split: {len(train_data)} training samples, {len(val_data)} validation samples.")
