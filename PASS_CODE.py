import time
import os
import sys
import hashlib
import datetime

# --- UI CONSTANTS ---
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[97m"
COLOR_RESET = "\033[0m"
COLOR_DIM = "\033[2m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, min_delay=0.01, max_delay=0.03, end=""):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    sys.stdout.write(end)
    sys.stdout.flush()

class NuclearCodeGenerator:
    def __init__(self):
        self.base_seed = int(time.time() / 300)
    
    def generate_commit_code(self):
        seed = f"COMMIT_{self.base_seed}_{int(time.time()/60)}".encode()
        return hashlib.sha256(seed).hexdigest()[:8].upper()
    
    def generate_abort_code(self):
        seed = f"ABORT_{self.base_seed}_{int(time.time()/60)}".encode()
        return hashlib.sha256(seed).hexdigest()[:8].upper()
    
    def generate_code(self, nation):
        seed = f"{nation}_{self.base_seed}".encode()
        return hashlib.sha256(seed).hexdigest()[:12].upper()

def authenticate_user():
    clear_screen()
    print(f"{COLOR_RED}AUTHENTICATION REQUIRED{COLOR_RESET}")
    sys.stdout.write(f"{COLOR_WHITE}OPERATOR ID: {COLOR_BLUE}")
    sys.stdout.flush()
    user = input().strip()
    if user != "MR_WOLF":
        print(f"\n{BG_RED}{COLOR_WHITE} ACCESS DENIED {COLOR_RESET}")
        time.sleep(2)
        return False
    
    sys.stdout.write(f"{COLOR_WHITE}SECURITY CODE: {COLOR_BLUE}")
    sys.stdout.flush()
    import msvcrt
    passcode = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter key
            break
        elif char == b'\x08':  # Backspace
            if passcode:
                passcode = passcode[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            passcode += char.decode('utf-8')
            sys.stdout.write('*')
            sys.stdout.flush()
    
    if passcode != "WOLF!(@)":
        print(f"\n{BG_RED}{COLOR_WHITE} INVALID SECURITY CODE {COLOR_RESET}")
        time.sleep(2)
        return False
    
    return True

def display_disclaimer():
    clear_screen()
    print(f"{COLOR_RED}{'='*80}{COLOR_RESET}")
    print(f"{COLOR_WHITE}{'W.O.L.F. CORPORATION - CLASSIFIED SYSTEM':^80}{COLOR_RESET}")
    print(f"{COLOR_RED}{'='*80}{COLOR_RESET}")
    time.sleep(1)

def log(msg, level="INFO", timestamp=None):
    ts = timestamp if timestamp else datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    color = COLOR_GREEN if level == "INFO" else COLOR_YELLOW if level == "WARN" else COLOR_RED if level == "ERROR" else COLOR_CYAN
    label = f"[{ts}] [{level}]"
    print(f"{color}{label:<18}{COLOR_RESET} {msg}")

def display_wolf_corp_screen():
    clear_screen()
    banner = [
        "██╗    ██╗ ██████╗ ██╗     ███████╗",
        "██║    ██║ ██╔══██╗██║     ██╔════╝",
        "██║ █╗ ██║ ██████╔╝██║     █████╗  ",
        "██║███╗██║ ██╔══██╗██║     ██╔══╝  ",
        "╚███╔███╔╝ ██████╔╝███████╗██║     ",
        " ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝     "
    ]
    print(COLOR_RED)
    for line in banner:
        print(line.center(80))
    print(f"\n{COLOR_WHITE}{'W.O.L.F. CORPORATION':^80}{COLOR_RESET}")
    time.sleep(1)

import json
import os

# Shared seed file for synchronized random codes
SEED_FILE = "current_seed.json"

def get_shared_seed():
    """Get or create shared seed for synchronized random codes."""
    if os.path.exists(SEED_FILE):
        with open(SEED_FILE, 'r') as f:
            data = json.load(f)
            # Check if seed is from current 5-minute slot
            current_slot = int(time.time() / 300)
            if data.get('slot') == current_slot:
                return data.get('seed')
    
    # Generate new seed for current slot
    import random
    new_seed = random.randint(100000, 999999)
    current_slot = int(time.time() / 300)
    
    # Save new seed
    with open(SEED_FILE, 'w') as f:
        json.dump({'slot': current_slot, 'seed': new_seed}, f)
    
    return new_seed

def get_dynamic_codes():
    """Generates time-based codes valid for 5-minute slots using shared random seed."""
    # Use the same time slot calculation for both programs
    current_time = int(time.time())
    slot = current_time // 300  # 5-minute slots
    shared_seed = get_shared_seed()
    
    # Use consistent seed generation
    alpha_seed = f"WOLF_ALPHA_{slot}_{shared_seed}".encode()
    bravo_seed = f"WOLF_BRAVO_{slot}_{shared_seed}".encode()
    
    alpha_code = hashlib.sha256(alpha_seed).hexdigest()[:6].upper()
    bravo_code = hashlib.sha256(bravo_seed).hexdigest()[:6].upper()
    
    time_left = 300 - (current_time % 300)
    return alpha_code, bravo_code, time_left

def alpha_decoder():
    """Separate ALPHA decoder function"""
    clear_screen()
    print(f"{COLOR_RED}{'='*80}")
    print(f"{COLOR_RED}{'*** ALPHA DECODER ***':^80}")
    print(f"{COLOR_RED}{'='*80}")
    
    alpha_code, bravo_code, time_left = get_dynamic_codes()
    print(f"{COLOR_WHITE}{'Generated ALPHA Code:':^80}")
    print(f"{COLOR_GREEN}{alpha_code:^80}")
    print(f"{COLOR_YELLOW}{'Time Remaining: ' + str(time_left) + ' seconds':^80}")
    print(f"{COLOR_DIM}{'Use this ALPHA code in WOLF_OS':^80}")
    return alpha_code

def bravo_decoder():
    """Separate BRAVO decoder function"""
    clear_screen()
    print(f"{COLOR_RED}{'='*80}")
    print(f"{COLOR_RED}{'*** BRAVO DECODER ***':^80}")
    print(f"{COLOR_RED}{'='*80}")
    
    alpha_code, bravo_code, time_left = get_dynamic_codes()
    print(f"{COLOR_WHITE}{'Generated BRAVO Code:':^80}")
    print(f"{COLOR_GREEN}{bravo_code:^80}")
    print(f"{COLOR_YELLOW}{'Time Remaining: ' + str(time_left) + ' seconds':^80}")
    print(f"{COLOR_DIM}{'Use this BRAVO code in WOLF_OS':^80}")
    return bravo_code

def login():
    clear_screen()
    print(COLOR_RED)
    banner = [
        "██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ ",
        "██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗",
        "██║  ██║█████╗  ██║     ██║   ██║██║  ██║█████╗  ██████╔╝",
        "██║  ██║██╔══╝  ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗",
        "██████╔╝███████╗╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║",
        "╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    for b in banner: print(b.center(80))
    print(f"\n{'SECURE STRATEGIC CODE DECODER':^80}")
    print(f"{'='*80}{COLOR_RESET}")
    
    prompt_id = "OPERATOR ID: "
    sys.stdout.write(COLOR_WHITE + prompt_id.rjust(40 + len(prompt_id)//2))
    sys.stdout.write(COLOR_BLUE)
    sys.stdout.flush()
    user = input().strip()
    
    if user != "MR_WOLF":
        print(f"\n{BG_RED}{COLOR_WHITE} ACCESS DENIED. UNAUTHORIZED ATTEMPT LOGGED. {COLOR_RESET}".center(80))
        time.sleep(2)
        return False
    return True

def main():
    if not login():
        return
        
    try:
        while True:
            alpha, bravo, t_left = get_dynamic_codes()
            clear_screen()
            print(COLOR_RED)
            header = [
                " ▗▄▄▄  ▗▄▄▄▖ ▗▄▄▖ ▗▄▄▄▖ ▗▄▄▄  ▗▄▄▄▖ ▗▄▄▖ ",
                " ▐▌  █ ▐▌   ▐▌   ▐▌   █ ▐▌  █ ▐▌   ▐▌ █ ",
                " ▐▌  █ ▐▛▀▀▖▐▌   ▐▌   █ ▐▌  █ ▐▛▀▀▖▐▛▀▚ ",
                " ▐▙▄▄▀ ▐▙▄▄▖▝▚▄▄▖▝▚▄▄▄▀ ▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌"
            ]
            for h in header: print(h.center(80))
            print(f"\n{COLOR_WHITE}{'STRATEGIC DECODER ACTIVE':^80}")
            print(f"{'='*80}{COLOR_RESET}")
            
            print(f"{COLOR_WHITE}{'CURRENT TIMESTAMP: ' + COLOR_CYAN + datetime.datetime.now().strftime('%H:%M:%S'):^90}")
            print(f"{COLOR_WHITE}{'REGENERATION CYCLE: ' + COLOR_YELLOW + str(t_left) + ' SECONDS':^90}\n")
            
            print(f"{COLOR_WHITE}{'PHASE ALPHA CODE: ' + COLOR_RED + alpha:^90}")
            print(f"{COLOR_WHITE}{'PHASE BRAVO CODE: ' + COLOR_RED + bravo:^90}\n")

            
            print(f"{BG_RED}{COLOR_WHITE} CAUTION: CODES ARE SINGLE-USE WITHIN THE PERMITTED WINDOW. {COLOR_RESET}".center(80))
            print("\n" + f"{COLOR_DIM}PRESS CTRL+C TO TERMINATE SECURE SESSION.{COLOR_RESET}".center(80))
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{COLOR_RED}SESSION TERMINATED.{COLOR_RESET}".center(80))


if __name__ == "__main__":
    main()
