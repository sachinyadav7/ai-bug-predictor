import requests
import json
import time

url = "http://localhost:8000/api/v1/predict"

user_buggy_code = """
class UserService {
    static class User {
        String name;
        User(String name) {
            this.name = name;
        }
    }

    public static int getUserNameLength(User user) {
        // BUG 1: No null check for user
        if (user.name.equals("")) {
            return 0;
        }

        // BUG 2: Off-by-one error
        return user.name.length() + 1;
    }

    public static void main(String[] args) {
        User u = null;
        System.out.println(getUserNameLength(u));
    }
}
"""

print(f"Waiting for server to reload...")
time.sleep(3)

print(f"\n--- Testing User Java Code ---")
try:
    response = requests.post(url, json={"code": user_buggy_code, "language": "java"})
    if response.status_code == 200:
        data = response.json()
        print(f"Risk Score: {data['file_risk_score']:.2f} ({data['results'][0]['risk_level']})")
        
        for func in data['results']:
            print(f"Function: {func['function_name']}")
            if func.get('highlighted_tokens'):
                print(f"  - Heuristics: {[t['token'] for t in func['highlighted_tokens']]}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(e)
