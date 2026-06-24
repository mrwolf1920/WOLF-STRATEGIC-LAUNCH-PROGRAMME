import sys
import os

def check_module(module_name):
    print(f"Checking {module_name}...", end=" ")
    try:
        if module_name == "PLAY WAR":
            import importlib
            importlib.import_module("PLAY WAR".replace(" ", "_")) # wait, i renamed it to PLAY_WAR_TEMP earlier? no.
        else:
            __import__(module_name)
        print("OK")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    print(f"--- SYSTEM INTEGRITY CHECK ---")
    print(f"CWD: {os.getcwd()}")
    print(f"PYTHON: {sys.executable}")
    
    # Check PASS_CODE first
    if not check_module("PASS_CODE"):
        sys.exit(1)
        
    # Check world_data
    if not check_module("world_data"):
        sys.exit(1)

    # Check WOLF_DECODER
    if not check_module("WOLF_DECODER"):
        sys.exit(1)

    print("--- INTEGRITY CHECK COMPLETE: SYSTEM CLEAN ---")
