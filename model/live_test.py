"""
Live Testing Script for Bug Predictor Model
=============================================
Loads the trained model and runs 50+ diverse test cases,
computing accuracy, precision, recall, F1-score, and
per-category analysis with confidence scores.
"""

import torch
import json
import os
import sys
from collections import defaultdict
from transformers import RobertaTokenizer

# Add project root for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train import BugPredictor


# ---------------------------------------------------------------------------
# TEST CASES — diverse examples NEVER seen in training
# ---------------------------------------------------------------------------
TEST_CASES = [
    # ===== BUGGY CODE (label=1) =====
    
    # Null dereference
    {"code": """def get_user_name(user_dict):
    profile = user_dict.get("profile")
    # Bug: profile could be None
    return profile["first_name"]""", "label": 1, "category": "null_deref"},
    
    {"code": """def find_max(values):
    best = None
    for v in values:
        if best is None or v > best:
            best = v
    return best.real""", "label": 1, "category": "null_deref"},
    
    {"code": """def lookup(registry, key):
    entry = registry.get(key)
    return entry.value""", "label": 1, "category": "null_deref"},

    # Division by zero
    {"code": """def percentage(count, total):
    return (count / total) * 100""", "label": 1, "category": "div_by_zero"},
    
    {"code": """def avg_score(grades):
    return sum(grades) / len(grades)""", "label": 1, "category": "div_by_zero"},
    
    {"code": """def normalize(values):
    mx = max(values) - min(values)
    return [v / mx for v in values]""", "label": 1, "category": "div_by_zero"},
    
    # Index out of bounds
    {"code": """def get_third(items):
    return items[2]""", "label": 1, "category": "index_oob"},
    
    {"code": """def swap_first_last(arr):
    arr[0], arr[len(arr)] = arr[len(arr)], arr[0]
    return arr""", "label": 1, "category": "index_oob"},
    
    {"code": """def parse_csv_row(line):
    cols = line.split(",")
    return cols[0], cols[1], cols[2], cols[3]""", "label": 1, "category": "index_oob"},

    # Resource leak
    {"code": """def count_lines(path):
    f = open(path, "r")
    lines = f.readlines()
    return len(lines)""", "label": 1, "category": "resource_leak"},
    
    {"code": """def append_log(msg):
    f = open("app.log", "a")
    f.write(msg + "\\n")""", "label": 1, "category": "resource_leak"},
    
    {"code": """def read_binary(path):
    fh = open(path, "rb")
    data = fh.read()
    return data""", "label": 1, "category": "resource_leak"},

    # SQL injection
    {"code": """def get_user(name):
    import sqlite3
    conn = sqlite3.connect("db.sqlite")
    q = "SELECT * FROM users WHERE name = '" + name + "'"
    return conn.execute(q).fetchone()""", "label": 1, "category": "sql_injection"},
    
    {"code": """def delete_record(rid):
    import sqlite3
    conn = sqlite3.connect("db.sqlite")
    conn.execute(f"DELETE FROM records WHERE id = {rid}")
    conn.commit()""", "label": 1, "category": "sql_injection"},

    # Eval injection
    {"code": """def calculator(expr):
    return eval(expr)""", "label": 1, "category": "eval_injection"},
    
    {"code": """def run_user_code(code):
    exec(code)""", "label": 1, "category": "eval_injection"},
    
    {"code": """def dynamic_import(module_name):
    mod = __import__(module_name)
    return eval(f"mod.{module_name}")""", "label": 1, "category": "eval_injection"},

    # Infinite loop
    {"code": """def drain_queue(q):
    while True:
        item = q.get()
        process(item)""", "label": 1, "category": "infinite_loop"},
    
    {"code": """def countdown(n):
    while n > 0:
        print(n)
        # forgot n -= 1""", "label": 1, "category": "infinite_loop"},

    # Hardcoded secret
    {"code": """def connect_db():
    password = "supersecret123"
    return mysql.connect(host="db.prod", password=password)""", "label": 1, "category": "hardcoded_secret"},
    
    {"code": """def get_api_token():
    token = "ghp_abc123def456ghi789jkl012mno345pqr"
    return token""", "label": 1, "category": "hardcoded_secret"},

    # Empty catch
    {"code": """def safe_parse(data):
    try:
        return json.loads(data)
    except:
        pass""", "label": 1, "category": "empty_catch"},
    
    {"code": """def load_config(path):
    try:
        return yaml.safe_load(open(path))
    except Exception:
        return None""", "label": 1, "category": "empty_catch"},

    # Off-by-one
    {"code": """def sum_range(arr, start, end):
    total = 0
    for i in range(start, end + 2):
        total += arr[i]
    return total""", "label": 1, "category": "off_by_one"},

    # Missing return
    {"code": """def classify(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    # missing return for score < 70""", "label": 1, "category": "missing_return"},
    
    {"code": """def build_response(data, status):
    response = {"data": data, "status": status}
    # forgot to return response""", "label": 1, "category": "missing_return"},

    # Boolean logic error
    {"code": """def can_vote(age, is_citizen):
    if age >= 18 or is_citizen:
        return True
    return False""", "label": 1, "category": "bool_error"},

    # Type confusion
    {"code": """def format_price(price):
    return "$" + price""", "label": 1, "category": "type_confusion"},

    # Uninitialized variable
    {"code": """def select_winner(candidates):
    for c in candidates:
        if c.score > 90:
            winner = c
    return winner.name""", "label": 1, "category": "uninitialized_var"},

    # ===== CLEAN CODE (label=0) =====
    
    # Proper error handling
    {"code": """def read_json_file(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in {path}")
        return None""", "label": 0, "category": "error_handling"},
    
    {"code": """def safe_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b""", "label": 0, "category": "safe_compute"},
    
    {"code": """def safe_average(numbers):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)""", "label": 0, "category": "safe_compute"},

    # Context managers
    {"code": """def write_data(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True""", "label": 0, "category": "context_manager"},
    
    {"code": """def read_lines(filepath):
    with open(filepath, "r") as f:
        return f.readlines()""", "label": 0, "category": "context_manager"},
    
    {"code": """def copy_file(src, dst):
    with open(src, "rb") as inf:
        with open(dst, "wb") as outf:
            outf.write(inf.read())""", "label": 0, "category": "context_manager"},

    # Input validation
    {"code": """def validate_email(email):
    import re
    pattern = r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email: {email}")
    return email.lower()""", "label": 0, "category": "input_validation"},
    
    {"code": """def validate_age(age):
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValueError(f"Invalid age: {age}")
    return age""", "label": 0, "category": "input_validation"},

    # Parameterized query
    {"code": """def find_user(name):
    import sqlite3
    with sqlite3.connect("app.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = ?", (name,))
        return cur.fetchone()""", "label": 0, "category": "param_query"},
    
    {"code": """def insert_record(name, email):
    import sqlite3
    with sqlite3.connect("app.db") as conn:
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()""", "label": 0, "category": "param_query"},

    # Safe access
    {"code": """def get_nested(data, *keys):
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current""", "label": 0, "category": "safe_access"},
    
    {"code": """def safe_index(lst, idx, default=None):
    if 0 <= idx < len(lst):
        return lst[idx]
    return default""", "label": 0, "category": "safe_access"},

    # Proper loops
    {"code": """def find_pairs(nums, target):
    seen = set()
    pairs = []
    for n in nums:
        complement = target - n
        if complement in seen:
            pairs.append((complement, n))
        seen.add(n)
    return pairs""", "label": 0, "category": "proper_loop"},

    # Secure patterns
    {"code": """def hash_password(password):
    import hashlib
    import secrets
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}" """, "label": 0, "category": "secure_func"},
    
    {"code": """def get_api_key():
    import os
    key = os.environ.get("API_KEY")
    if not key:
        raise EnvironmentError("API_KEY not configured")
    return key""", "label": 0, "category": "secure_func"},

    # Clean utility functions
    {"code": """def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result""", "label": 0, "category": "utility"},
    
    {"code": """def chunk_list(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]""", "label": 0, "category": "utility"},
    
    {"code": """def deduplicate(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result""", "label": 0, "category": "utility"},

    # Clean class
    {"code": """class Stack:
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self):
        if not self._items:
            return None
        return self._items[-1]""", "label": 0, "category": "clean_class"},
]


def load_model(model_path="best_model.pt"):
    """Load the trained model."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    if not os.path.exists(model_path):
        model_path = "last_model.pt"
    if not os.path.exists(model_path):
        print(f"ERROR: No model found at best_model.pt or last_model.pt")
        sys.exit(1)
    
    print(f"Loading model from {model_path}...")
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    
    model = BugPredictor()
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    threshold = checkpoint.get('threshold', 0.5)
    metrics = checkpoint.get('metrics', {})
    
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    
    print(f"Model loaded on {device}")
    print(f"Training threshold: {threshold:.4f}")
    if metrics:
        print(f"Training best F1: {metrics.get('f1', 'N/A')}")
    
    return model, tokenizer, device, threshold


def predict_single(model, tokenizer, device, code, threshold=0.5):
    """Predict on a single code snippet."""
    inputs = tokenizer(
        code,
        return_tensors='pt',
        max_length=512,
        padding='max_length',
        truncation=True
    )
    
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        logits = outputs['logits']
        probs = torch.softmax(logits, dim=1)
        prob_buggy = probs[0][1].item()
        pred = 1 if prob_buggy > threshold else 0
    
    return pred, prob_buggy


def run_live_test():
    """Run the full live test suite."""
    print("=" * 70)
    print("   BUG PREDICTOR — LIVE TESTING SUITE")
    print("=" * 70)
    print()
    
    # Load model
    model, tokenizer, device, threshold = load_model()
    # Use standard 0.5 threshold for balanced predictions
    threshold = 0.5
    print(f"Using threshold: {threshold}")
    print()
    
    # Run predictions
    print("-" * 70)
    print("INDIVIDUAL TEST RESULTS")
    print("-" * 70)
    
    correct = 0
    total = len(TEST_CASES)
    tp, fp, tn, fn = 0, 0, 0, 0 
    category_results = defaultdict(lambda: {"correct": 0, "total": 0, "probs": []})
    
    for i, case in enumerate(TEST_CASES):
        pred, prob = predict_single(model, tokenizer, device, case["code"], threshold)
        expected = case["label"]
        category = case["category"]
        
        is_correct = pred == expected
        if is_correct:
            correct += 1
        
        # Confusion matrix
        if expected == 1 and pred == 1: tp += 1
        elif expected == 0 and pred == 1: fp += 1
        elif expected == 0 and pred == 0: tn += 1
        elif expected == 1 and pred == 0: fn += 1
        
        # Category tracking
        category_results[category]["total"] += 1
        if is_correct:
            category_results[category]["correct"] += 1
        category_results[category]["probs"].append(prob)
        
        status = "✓ PASS" if is_correct else "✗ FAIL"
        expected_str = "BUGGY" if expected == 1 else "CLEAN"
        pred_str = "BUGGY" if pred == 1 else "CLEAN"
        
        # Show first line of code for brevity
        code_preview = case["code"].strip().split("\n")[0][:60]
        
        print(f"  [{status}] #{i+1:2d} | Expected: {expected_str:5s} | Pred: {pred_str:5s} | "
              f"Prob: {prob:.4f} | {code_preview}")
    
    # Compute metrics
    accuracy = correct / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print()
    print("=" * 70)
    print("   OVERALL METRICS")
    print("=" * 70)
    print(f"  Accuracy:   {accuracy:.2%}  ({correct}/{total})")
    print(f"  Precision:  {precision:.2%}")
    print(f"  Recall:     {recall:.2%}")
    print(f"  F1 Score:   {f1:.2%}")
    print(f"  Threshold:  {threshold:.4f}")
    print()
    
    print("  Confusion Matrix:")
    print(f"                  Predicted CLEAN  Predicted BUGGY")
    print(f"  Actual CLEAN         {tn:3d}             {fp:3d}")
    print(f"  Actual BUGGY         {fn:3d}             {tp:3d}")
    print()
    
    # Per-category breakdown
    print("=" * 70)
    print("   PER-CATEGORY BREAKDOWN")
    print("=" * 70)
    print(f"  {'Category':<22s} {'Correct':>8s} {'Total':>6s} {'Acc':>8s} {'Avg Prob':>10s}")
    print(f"  {'-'*22} {'-'*8} {'-'*6} {'-'*8} {'-'*10}")
    
    for cat in sorted(category_results.keys()):
        r = category_results[cat]
        cat_acc = r["correct"] / r["total"] if r["total"] > 0 else 0
        avg_prob = sum(r["probs"]) / len(r["probs"]) if r["probs"] else 0
        print(f"  {cat:<22s} {r['correct']:>8d} {r['total']:>6d} {cat_acc:>7.0%} {avg_prob:>10.4f}")
    
    print()
    print("=" * 70)
    
    # Also load and test from the test_full.jsonl file if it exists
    test_file = "data/test_full.jsonl"
    if os.path.exists(test_file):
        print()
        print("=" * 70)
        print("   TEST SET EVALUATION (data/test_full.jsonl)")
        print("=" * 70)
        
        with open(test_file, 'r') as f:
            test_data = [json.loads(line) for line in f]
        
        test_correct = 0
        test_tp = test_fp = test_tn = test_fn = 0
        test_cat_results = defaultdict(lambda: {"correct": 0, "total": 0})
        
        for item in test_data:
            pred, prob = predict_single(model, tokenizer, device, item["code"], threshold)
            expected = item["label"]
            category = item.get("category", "unknown")
            
            if pred == expected:
                test_correct += 1
                test_cat_results[category]["correct"] += 1
            
            test_cat_results[category]["total"] += 1
            
            if expected == 1 and pred == 1: test_tp += 1
            elif expected == 0 and pred == 1: test_fp += 1
            elif expected == 0 and pred == 0: test_tn += 1
            elif expected == 1 and pred == 0: test_fn += 1
        
        test_acc = test_correct / len(test_data) if test_data else 0
        test_prec = test_tp / (test_tp + test_fp) if (test_tp + test_fp) > 0 else 0
        test_rec = test_tp / (test_tp + test_fn) if (test_tp + test_fn) > 0 else 0
        test_f1 = 2 * test_prec * test_rec / (test_prec + test_rec) if (test_prec + test_rec) > 0 else 0
        
        print(f"  Test samples: {len(test_data)}")
        print(f"  Accuracy:     {test_acc:.2%}  ({test_correct}/{len(test_data)})")
        print(f"  Precision:    {test_prec:.2%}")
        print(f"  Recall:       {test_rec:.2%}")
        print(f"  F1 Score:     {test_f1:.2%}")
        print()
        
        print(f"  {'Category':<22s} {'Correct':>8s} {'Total':>6s} {'Acc':>8s}")
        print(f"  {'-'*22} {'-'*8} {'-'*6} {'-'*8}")
        for cat in sorted(test_cat_results.keys()):
            r = test_cat_results[cat]
            cat_acc = r["correct"] / r["total"] if r["total"] > 0 else 0
            print(f"  {cat:<22s} {r['correct']:>8d} {r['total']:>6d} {cat_acc:>7.0%}")
        
        print("=" * 70)
    
    return accuracy, precision, recall, f1


if __name__ == "__main__":
    accuracy, precision, recall, f1 = run_live_test()
    print(f"\nFinal Summary: Accuracy={accuracy:.2%}, F1={f1:.2%}")
