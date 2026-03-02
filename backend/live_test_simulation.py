import requests
import json
import time

def live_test():
    url = "http://localhost:8000/api/v1/predict"
    
    # Test cases mirroring verify_model.py logic but via API
    test_cases = [
        {
            "code": "def buggy(x):\n    if x = 10:\n        print('Error')",
            "desc": "Comparison Error (Syntax)",
            "expected_buggy": True
        },
        {
            "code": "def clean(x):\n    if x == 10:\n        print('Ok')",
            "desc": "Clean Code",
            "expected_buggy": False
        }
    ]
    
    print(f"Testing API at {url}...")
    
    for case in test_cases:
        payload = {
            "code": case["code"],
            "language": "python",
            "filename": "test.py",
            "include_explanation": True
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                bug_count = result.get("buggy_functions_count", 0)
                is_buggy = bug_count > 0
                
                status = "PASS" if is_buggy == case["expected_buggy"] else "FAIL"
                print(f"[{status}] {case['desc']}")
                print(f"  Prediction: Buggy={is_buggy} (Count={bug_count})")
                
                # Check individual function results
                if result.get("results"):
                    for func_res in result["results"]:
                         print(f"    Function '{func_res['function_name']}': Buggy={func_res['is_buggy']}, Conf={func_res['confidence']:.4f}")
            else:
                print(f"[ERROR] {case['desc']} - Status {response.status_code}")
                print(response.text)
        except requests.exceptions.ConnectionError:
             print(f"[ERROR] Could not connect to server at {url}. Is it running?")
        except Exception as e:
            print(f"[ERROR] Exception: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    live_test()
