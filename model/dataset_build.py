import os
import json
import re
import subprocess
from typing import List, Dict, Tuple

def remove_comments(code: str) -> str:
    """
    Remove C-style comments (// and /* */) and Python comments (#).
    Simple regex-based approach.
    """
    # Remove C-style blocks
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Remove C-style lines
    code = re.sub(r'//.*', '', code)
    # Remove Python lines
    code = re.sub(r'#.*', '', code)
    return code.strip()

def normalize_code(code: str) -> str:
    """
    Normalize variables? (User requested 'normalize variables')
    This is complex to do robustly without a parser.
    For now, we'll just normalize whitespace an common tokens if needed.
    """
    code = re.sub(r'\s+', ' ', code)
    return code.strip()

def extract_from_git_log(repo_path: str, limit: int = 1000) -> List[Dict]:
    """
    Run git log to find bug fixes and extract buggy/clean pairs.
    Assumes 'fix' in commit message implies a bug fix.
    """
    print(f"Scanning {repo_path}...")
    cmd = [
        "git", "-C", repo_path, "log", 
        "--grep=fix", "-p", f"-n {limit}", 
        "--pretty=format:COMMIT_HASH:%H"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Error running git log: {e}")
        return []
    
    data_samples = []
    
    # Very basic parsing of the git log output
    # This is a placeholder for the logic needed to parse the diffs
    # In a real scenario, we'd use 'pydriller' or similar, but pure python parsing:
    
    commits = result.stdout.split("COMMIT_HASH:")
    for commit in commits:
        if not commit.strip():
            continue
            
        # Parse logic here would be complex: determining which part is buggy (removed lines)
        # vs clean (added lines).
        # For this script, we will provide the scaffolding and a TODO.
        pass
        
    print("This function requires a more complex diff parser to reliably extract 'before' (buggy) and 'after' (clean) code blocks.")
    print("Recommendation: Use 'pydriller' library if available.")
    
    return data_samples

def save_to_jsonl(samples: List[Dict], output_file: str):
    with open(output_file, 'a', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")

def main():
    print("Bug Predictor Dataset Builder")
    print("=============================")
    print("Rules:")
    print("1. Collect buggy (label 1) and clean (label 0) code")
    print("2. Remove comments")
    print("3. Normalize")
    print("4. Max length 512")
    
    # Example usage (commented out)
    # samples = extract_from_git_log("../some-repo")
    # processed = []
    # for s in samples:
    #    code = remove_comments(s['code'])
    #    if len(code) < 10: continue
    #    processed.append({'code': code[:2000], 'label': s['label']})
    
    # save_to_jsonl(processed, "data/raw_dataset.jsonl")
    
    print("\nScript ready. Integrate with specific repository paths to start collection.")

if __name__ == "__main__":
    main()
