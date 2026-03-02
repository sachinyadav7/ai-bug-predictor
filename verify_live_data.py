
import requests
import time
import sys
import os

# Add backend to path to use ModelManager directly if needed, 
# but we should test the API if server is running.
# The server is running at localhost:8000

BASE_URL = "http://localhost:8000/api/v1"

def test_stats_integration():
    print("1. Fetching initial stats...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/stats", timeout=5)
        if response.status_code != 200:
             print(f"Error: Server returned {response.status_code}")
             return
        initial_stats = response.json()
        print(f"Initial Stats: {initial_stats}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to server. Make sure it is running. Details: {e}")
        return

    print("\n2. Running a prediction (simulation)...")
    payload = {
        "code": "def loop():\n    while True:\n        print('Loop')",
        "language": "python"
    }
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        prediction = response.json()
        print(f"Prediction result: Buggy={prediction['buggy_functions_count'] > 0}")
    except Exception as e:
        print(f"Prediction failed: {e}")
        return

    print("\n3. Fetching updated stats...")
    time.sleep(1) # Give it a moment (though it's synchronous usually)
    try:
        response = requests.get(f"{BASE_URL}/dashboard/stats")
        updated_stats = response.json()
        print(f"Updated Stats: {updated_stats}")
        
        # Verification
        if updated_stats['total_scans'] > initial_stats['total_scans']:
            print("\nSUCCESS: Total scans increased.")
        else:
            print("\nFAILURE: Total scans did not increase.")
            
        if len(updated_stats['recent_scans']) > 0:
             print("SUCCESS: Recent scans populated.")
        else:
             print("FAILURE: Recent scans empty.")
             
    except Exception as e:
        print(f"Failed to fetch updated stats: {e}")

if __name__ == "__main__":
    test_stats_integration()
