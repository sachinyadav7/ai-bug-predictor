import json
import random

buggy_patterns = [
    "def divide(a,b): return a/b # Potential division by zero",
    "arr=[1,2]; print(arr[5]) # IndexError",
    "x=None; print(x.upper()) # AttributeError",
    "open('file.txt') # Resource leak, missing close",
    "while True: print('loop') # Infinite loop",
    "def func(): return # Missing return value",
    "if x = 5: print(x) # SyntaxError",
    "password = '123456' # Security Risk",
    "eval('2 + 2') # Security Risk",
    "try: pass except: pass # Bare except",
]

clean_patterns = [
    "def add(a,b): return a+b",
    "for i in range(5): print(i)",
    "x='hello'; print(x.upper())",
    "with open('file.txt') as f: data=f.read()",
    "if x == 5: print(x)",
    "try: x=1/y except ZeroDivisionError: print('error')",
    "def secure_func(token): return token.hash()",
    "users = ['alice', 'bob']; print(users[0])",
    "import os; os.getenv('API_KEY')",
]

def make_dataset(n_samples):
    data = []
    for _ in range(n_samples):
        if random.random() < 0.5:
            code = random.choice(buggy_patterns)
            # Add some random variations (comments, whitespace)
            if random.random() > 0.5:
                code += f" # Random comment {random.randint(1, 100)}"
            data.append({"code": code, "label": 1})
        else:
            code = random.choice(clean_patterns)
            if random.random() > 0.5:
                code += f" # Safe code {random.randint(1, 100)}"
            data.append({"code": code, "label": 0})
    return data

train = make_dataset(10000)
val = make_dataset(2000)

with open("data/train.jsonl","w") as f:
    for x in train:
        f.write(json.dumps(x)+"\n")

with open("data/val.jsonl","w") as f:
    for x in val:
        f.write(json.dumps(x)+"\n")

print("Synthetic dataset created")
