import requests
import json
import time

url = "http://localhost:8000/api/v1/predict"

def test_code(name, code, desc):
    print(f"\n--- Testing {name} ({desc}) ---")
    payload = {
        "code": code,
        "language": "python",
        "include_explanation": True
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            score = data['file_risk_score']
            print(f"File Risk Score: {score:.2f}")
            for func in data['results']:
                print(f"Function: {func['function_name']}")
                print(f"  - Buggy: {func['is_buggy']}")
                print(f"  - Risk: {func['risk_level']}")
                print(f"  - Confidence: {func['confidence']:.2%}")
                if func.get('highlighted_tokens'):
                    print(f"  - Detected: {[t['token'] for t in func['highlighted_tokens']]}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

# 1. Clean Code
clean_code = """
def add_numbers(a, b):
    # This is a safe function
    return a + b
"""

# 2. Buggy Code (Heuristic Trigger)
buggy_code = """
def unsafe_execution(user_input):
    # Dangerous usage
    eval(user_input)
    
    # Infinite loop risk
    while True:
        pass
"""

# Wait for server to start if we just relaunched it
print("Waiting for server...")
time.sleep(2)

test_code("Clean Code", clean_code, "Should be Low Risk")
test_code("Buggy Code", buggy_code, "Should be High Risk (Heuristics)")
