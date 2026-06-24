import sys
import os

# Add parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(f"--- Failsafe Integrity Check ---")
print(f"CWD: {os.getcwd()}")

try:
    import data.world_data as world_data
    print("✓ world_data found")
except Exception as e:
    print(f"✗ ERROR IMPORTING world_data: {e}")

try:
    import core.WOLF_OS as WOLF_OS
    print("✓ WOLF_OS compiled successfully")
except Exception as e:
    print(f"✗ ERROR IN WOLF_OS: {e}")
    import traceback
    traceback.print_exc()

input("\nPRESS ENTER TO CONTINUE")
