
import sys
import os

print("Starting debug script...")
try:
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    print("Added backend to path.")
    from app.core.model import model_manager
    print("Imported model_manager successfully.")
except Exception as e:
    print(f"Import failed: {e}")
