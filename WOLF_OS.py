import time
import sys
import random
import os

from pathlib import Path

# Robustly add project root to sys.path (Fixes Mac/Linux import errors)
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import urllib.request
import json
import ssl
import socket
import subprocess
import ctypes
import hashlib
import datetime
import data.world_data as world_data
from core.PASS_CODE import (
    NuclearCodeGenerator, COLOR_RED, COLOR_GREEN, COLOR_BLUE, 
    COLOR_WHITE, COLOR_RESET, COLOR_YELLOW, COLOR_DIM, COLOR_CYAN, 
    BG_RED, clear_screen, type_text, authenticate_user, 
    display_disclaimer, display_wolf_corp_screen, log, get_shared_seed, get_dynamic_codes
)
import socket
import threading
from core.CRYPTO import MilitaryCryptoManager

# Initialize Encryption Manager
crypto_mgr = MilitaryCryptoManager()
import json
import time as time_module

# --- GEOPOLITICAL MAPPING ---
CONTINENT_MAPPING = {
    "NORTH AMERICA": ["UNITED STATES", "CANADA", "MEXICO", "ANTIGUA AND BARBUDA", "BAHAMAS", "BARBADOS", "BELIZE", "COSTA RICA", "CUBA", "DOMINICA", "DOMINICAN REPUBLIC", "EL SALVADOR", "GRENADA", "GUATEMALA", "HAITI", "HONDURAS", "JAMAICA", "NICARAGUA", "PANAMA", "SAINT KITTS AND NEVIS", "SAINT LUCIA", "SAINT VINCENT AND THE GRENADINES", "TRINIDAD AND TOBAGO"],
    "SOUTH AMERICA": ["ARGENTINA", "BOLIVIA", "BRAZIL", "CHILE", "COLOMBIA", "ECUADOR", "GUYANA", "PARAGUAY", "PERU", "SURINAME", "URUGUAY", "VENEZUELA"],
    "EUROPE": ["UNITED KINGDOM", "FRANCE", "RUSSIA", "GERMANY", "GEORGIA", "GREECE", "HUNGARY", "ICELAND", "IRELAND", "ITALY", "KAZAKHSTAN", "LATVIA", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG", "MALTA", "MOLDOVA", "MONACO", "MONTENEGRO", "NETHERLANDS", "NORTH MACEDONIA", "NORWAY", "POLAND", "PORTUGAL", "ROMANIA", "SAN MARINO", "SERBIA", "SLOVAKIA", "SLOVENIA", "SPAIN", "SWEDEN", "SWITZERLAND", "UKRAINE", "VATICAN CITY"],
    "ASIA": ["CHINA", "INDIA", "PAKISTAN", "NORTH KOREA", "ISRAEL", "AFGHANISTAN", "ARMENIA", "AZERBAIJAN", "BAHRAIN", "BANGLADESH", "BHUTAN", "BRUNEI", "CAMBODIA", "CYPRUS", "EAST TIMOR", "INDONESIA", "IRAN", "IRAQ", "JAPAN", "JORDAN", "KUWAIT", "KYRGYZSTAN", "LAOS", "LEBANON", "MALAYSIA", "MALDIVES", "MONGOLIA", "MYANMAR", "NEPAL", "OMAN", "PHILIPPINES", "QATAR", "SAUDI ARABIA", "SINGAPORE", "SOUTH KOREA", "SRI LANK", "SYRIA", "TAIWAN", "TAJIKISTAN", "THAILAND", "TURKEY", "TURKMENISTAN", "UNITED ARAB EMIRATES", "UZBEKISTAN", "VIETNAM", "YEMEN"],
    "AFRICA": ["ANGOLA", "ALGERIA", "BENIN", "BOTSWANA", "BURKINA FASO", "BURUNDI", "CAMEROON", "CAPE VERDE", "CENTRAL AFRICAN REPUBLIC", "CHAD", "COMOROS", "CONGO", "DJIBOUTI", "EGYPT", "EQUATORIAL GUINEA", "ERITREA", "ETHIOPIA", "GABON", "GAMBIA", "GHANA", "GUINEA", "GUINEA-BISSAU", "IVORY COAST", "KENYA", "LESOTHO", "LIBERIA", "LIBYA", "MADAGASCAR", "MALAWI", "MALI", "MAURITANIA", "MAURITIUS", "MOROCCO", "MOZAMBIQUE", "NAMIBIA", "NIGER", "NIGERIA", "RWANDA", "SAO TOME AND PRINCIPE", "SENEGAL", "SEYCHELLES", "SIERRA LEONE", "SOMALIA", "SOUTH AFRICA", "SOUTH SUDAN", "SUDAN", "SWAZILAND", "TANZANIA", "TOGO", "TUNISIA", "UGANDA", "ZAMBIA", "ZIMBABWE"],
    "AUSTRALIA": ["AUSTRALIA", "FIJI", "KIRIBATI", "MARSHALL ISLANDS", "MICRONESIA", "NAURU", "NEW ZEALAND", "PALAU", "PAPUA NEW GUINEA", "SAMOA", "SOLOMON ISLANDS", "TONGA", "TUVALU", "VANUATU"]
}

def get_nation_continent(nation: str) -> str:
    for continent, countries in CONTINENT_MAPPING.items():
        if nation.upper() in [c.upper() for c in countries]:
            return continent
    return "UNKNOWN"

if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

try:
    import tty, termios
except ImportError:
    tty = None
    termios = None

def getch():
    if os.name == 'nt':
        try:
            return msvcrt.getch().decode('utf-8', 'ignore')
        except:
            return ""
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def clear_screen():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

def breach_protocol_initiated():
    """Display breach protocol error message and terminate program"""
    print(f"\n{BG_RED}{COLOR_WHITE}{'!!! ABORTED !!! BREACH PROTOCOL INITIATED':^80}{COLOR_RESET}")
    print(f"{BG_RED}{COLOR_WHITE}{'SECURITY BREACH DETECTED - SYSTEM LOCKDOWN ENGAGED':^80}{COLOR_RESET}")
    print(f"{BG_RED}{COLOR_WHITE}{'ALL OPERATIONS SUSPENDED - AWAITING MANUAL OVERRIDE':^80}{COLOR_RESET}")
    print(f"{BG_RED}{COLOR_WHITE}{'SYSTEM TERMINATION INITIATED...':^80}{COLOR_RESET}\n")
    time.sleep(2.0)
    exit()

def get_blind_input(prompt: str = ""):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    password = ""
    while True:
        char = getch()
        if char in ['\r', '\n']:
            print()
            break
        elif char in ['\b', '\x08', '\x7f']:
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write('*')
            sys.stdout.flush()
    return password.strip()

from typing import Optional, Dict, List
import data.world_data as world_data

# --- GLOBAL UI CONSTANTS ---
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[97m"
COLOR_DIM = "\033[2m"
COLOR_BLINK = "\033[5m"
COLOR_RESET = "\033[0m"
BG_RED = "\033[41m"
BG_WHITE = "\033[47m"

def update_nuclear_weapons_database():
    """Update nuclear weapons database with real-time data"""
    print(f"{COLOR_YELLOW}[UPDATE] SYNCHRONIZING NUCLEAR ASSETS DATABASE...{COLOR_RESET}")
    
    # Real-time nuclear weapons data (updated with current deployments)
    global icbm_data, slbm_data, vessel_status
    
    # Update ICBM data with current operational status
    icbm_data = {
        # UNITED STATES - Current operational status
        "LGM-30G MINUTEMAN III": f"US ICBM, 400 active silos, 170-335 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "LGM-118A PEACEKEEPER": "US ICBM, Retired 2005 - Status: NADA",
        "MX MISSILE": "US ICBM, Cancelled 1992 - Status: NADA",
        "MINUTEMAN III": f"US ICBM, 400 operational, W62 warheads - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        
        # RUSSIA - Current operational status
        "RS-28 SARMAT": f"Russian ICBM, 50 deployed, 10.5 MT - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        "RS-24 YARS": f"Russian ICBM, 150 mobile launchers, 1.2 MT - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "RT-2PM2 TOPOL-M": f"Russian ICBM, 100 operational, 100 MT capability - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        "R-36M2 VOEVODA": f"Russian ICBM, 46 silos, 8 MT - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        "UR-100N STILETTO": f"Russian ICBM, 30 operational, 6 MT - Status: {random.choice(['MEH', 'NADA'])}",
        
        # CHINA - Current operational status
        "DF-5B": f"Chinese ICBM, 20 silos, 5 MT - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        "DF-31A": f"Chinese ICBM, 50 mobile, 3 MT - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "DF-31AG": f"Chinese ICBM, 30 advanced, 2.8 MT - Status: {random.choice(['WILCO', 'MEH'])}",
        "DF-41": f"Chinese ICBM, 15 deployed, 12 MT - Status: {random.choice(['MEH', 'NADA'])}",
        
        # FRANCE - SLBM only
        "M51.2": f"French SLBM, 48 missiles, 150 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "M51.3": f"French SLBM, 12 missiles, 200 kt - Status: {random.choice(['WILCO', 'MEH'])}",
        
        # UK - SLBM only
        "UGM-133A TRIDENT II D5 UK": f"UK SLBM, 40 missiles, 475 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        
        # INDIA - Current operational status
        "AGNI-V": f"Indian ICBM, 20 operational, 2.5 MT, 5,000+ km - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        
        # PAKISTAN - Current operational status
        "SHAHEEN-III": f"Pakistani ICBM, 15 operational, 1.8 MT, 2,750 km - Status: {random.choice(['MEH', 'NADA'])}",
        
        # NORTH KOREA - Current operational status
        "HWASONG-14": f"North Korean ICBM, 5 operational, 1 MT - Status: {random.choice(['NADA', 'MEH'])}",
        "HWASONG-15": f"North Korean ICBM, 8 operational, 1 MT - Status: {random.choice(['NADA', 'MEH'])}",
        "HWASONG-17": f"North Korean ICBM, 3 operational, 1.5 MT - Status: {random.choice(['NADA'])}",
        
        # ISRAEL - Current operational status
        "JERICHO-III": f"Israeli ICBM, 25 operational, 750 kt - Status: {random.choice(['WILCO', 'MEH'])}",
    }
    
    # Update SLBM data with current deployments
    slbm_data = {
        "UGM-133A TRIDENT II D5": f"US SLBM, 336 missiles, 475 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "RSM-56 BULAVA": f"Russian SLBM, 160 missiles, 100 kt - Status: {random.choice(['WILCO', 'MEH', 'NADA'])}",
        "R-29RMU SINEVA": f"Russian SLBM, 96 missiles, 250 kt - Status: {random.choice(['MEH', 'NADA'])}",
        "JL-2": f"Chinese SLBM, 48 missiles, 200 kt - Status: {random.choice(['MEH', 'NADA'])}",
        "JL-3": f"Chinese SLBM, 12 missiles, 350 kt - Status: {random.choice(['NADA'])}",
        "M51.2": f"French SLBM, 48 missiles, 150 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "UGM-133A TRIDENT II D5 UK": f"UK SLBM, 40 missiles, 475 kt - Status: {random.choice(['WILCO', 'WILCO', 'MEH'])}",
        "K-4": f"Indian SLBM, 8 missiles, 1 MT - Status: {random.choice(['NADA', 'MEH'])}",
    }
    
    print(f"{COLOR_GREEN}[UPDATE] NUCLEAR ASSETS DATABASE SYNCHRONIZED{COLOR_RESET}")
    time.sleep(0.5)

def sync_live_population_data():
    cache_file = "live_census_cache.json"
    is_online = False
    test_urls = ["https://www.google.com", "https://8.8.8.8"]
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for url in test_urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=4) as response:
                if response.status in [200, 301, 302]:
                    is_online = True
                    break
        except Exception: continue
    if is_online:
        updated_world_data = {}
        for country, cities in world_data.WORLD_DATA.items():
            updated_world_data[country] = []
            for city in cities:
                new_city = dict(city)
                new_city["population"] += random.randint(12, 185)
                updated_world_data[country].append(new_city)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(updated_world_data, f)
        except: pass
        return updated_world_data, True
    else:
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f), False
            except: pass
        return world_data.WORLD_DATA, False

class DataManager:
    def __init__(self):
        self.base_populations = {}
        self.metro_to_core_ratio = {"NEW YORK": 0.43, "MOSCOW": 0.97, "LONDON": 0.59}
        self.nation_cities = {}
        self.target_etas = {"UNITED STATES": 30, "RUSSIA": 28, "CHINA": 28, "ISRAEL": 7}
        self.city_coordinates = {}
        self.live_world_data, self.is_online = sync_live_population_data()
        for country, cities in self.live_world_data.items():
            self.nation_cities[country] = [c["name"] for c in cities]
            for city in cities:
                self.base_populations[city["name"]] = city["population"] / 1000000.0
                self.city_coordinates[city["name"]] = (city["lat"], city["lon"])
        self.weapon_yields = {"LGM-30G MINUTEMAN III": 0.3, "RS-28 SARMAT": 1.0, "UGM-133 TRIDENT II": 0.475}

    def get_dynamic_population(self, city: str) -> dict:
        base_metro = self.base_populations.get(city.upper(), 1.0)
        metro_pop = base_metro * (1.0 + (datetime.datetime.now().second/6000.0))
        ratio = self.metro_to_core_ratio.get(city.upper(), 0.5)
        return {"city": city.upper(), "metro": int(metro_pop * 1_000_000), "core": int(metro_pop * ratio * 1_000_000)}

    def get_cities_for_nation(self, nation: str) -> list:
        cities = self.nation_cities.get(nation.upper(), [])
        return [(c, self.get_dynamic_population(c)["core"], self.get_dynamic_population(c)["metro"], self.target_etas.get(nation.upper(), 30), self.city_coordinates.get(c.upper(), (0,0))) for c in cities]

    def get_yield(self, weapon: str) -> float:
        for name, yld in self.weapon_yields.items():
            if name.upper() in weapon.upper(): return yld
        return 0.5

    def calculate_casualties(self, target_city: str, weapon_name: str) -> int:
        pop = self.get_dynamic_population(target_city)["metro"]
        yld = self.get_yield(weapon_name)
        if yld >= 1.0: rate = 0.65
        elif yld >= 0.8: rate = 0.45
        elif yld >= 0.4: rate = 0.35
        else: rate = 0.25
        return int(pop * rate)

class ScenarioEngine:
    def get_game_list(self) -> List[str]:
        return ["TIC-TAC-TOE", "CHESS", "GLOBAL THERMONUCLEAR WAR"]

def type_text(text: str, min_delay: float = 0.01, max_delay: float = 0.05, end: str = "\n"):
    i = 0
    while i < len(text):
        if text[i] == '\033' and i + 1 < len(text) and text[i+1] == '[':
            end_idx = text.find('m', i)
            if end_idx != -1:
                sys.stdout.write(text[i:end_idx+1])
                i = end_idx + 1; continue
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(random.uniform(min_delay, max_delay))
        i += 1
    sys.stdout.write(end); sys.stdout.flush()

def log(msg, level="INFO", timestamp=None):
    ts = timestamp if timestamp else datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    color = COLOR_GREEN if level == "INFO" else COLOR_YELLOW if level == "WARN" else COLOR_RED if level == "ERROR" else COLOR_CYAN
    label = f"[{ts}] [{level}]"
    print(f"{color}{label:<18}{COLOR_RESET} {msg}")

def system_boot_sequence():
    start_time = time.time()
    clear_screen()
    
    # Firmware header
    type_text(f"{COLOR_WHITE}W.O.L.F.{COLOR_RED} 8080 FIRMWARE {COLOR_YELLOW}V1.3.4{COLOR_RED}", 0.02, 0.05)
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    type_text(" // TIMESTAMP: " + ts, 0.01, 0.03)
    print(f"\n{COLOR_CYAN}[ BIOS DATE 03/19/26 20:52:31 VER 1.3.4 ]{COLOR_RESET}\n")
    time.sleep(0.3)
    
    # Phase 1: PRE-BOOT CHECKS
    print(f"\n{COLOR_WHITE}=== PRE-BOOT CHECKS ==={COLOR_RESET}")
    hardware = [
        ("CPU: Quantum Processor @ 8.4GHz", True),
        ("RAM: 32768MB DDR5 ECC", True),
        ("GPU: Neural Array Controller", True),
        ("NIC: Classified Mil-Spec Adapter", True),
        ("STORAGE: NVMe RAID 0 4TB", True),
        ("HSM: Hardware Security Module", True),
        ("Secondary telemetry array", False),  # Simulate failure
    ]
    for item, ok in hardware:
        if ok:
            type_text(f"{COLOR_GREEN}[ OK ]{COLOR_RESET} Detected {item}...", 0.003, 0.01)
            time.sleep(random.uniform(0.1, 0.3))
        else:
            type_text(f"{COLOR_RED}[FAIL]{COLOR_RESET} {item}...", 0.005, 0.02)
            time.sleep(0.5)
            type_text(f"{COLOR_YELLOW}[WARN]{COLOR_RESET}   Fallback to primary telemetry...", 0.005, 0.02)
            time.sleep(0.3)
    
    # Simulate anomaly
    if random.random() < 0.15:
        print(f"\n{COLOR_YELLOW}[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] [WARN] Clock desync detected. Resynchronizing...{COLOR_RESET}")
        time.sleep(1.2)
        print(f"{COLOR_GREEN}[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] [OK]   Time sync restored{COLOR_RESET}")
        time.sleep(0.2)
    
    # Interrupt
    if random.random() < 0.1:
        print(f"\n{BG_RED}{COLOR_WHITE}>>> INTERRUPT: External signal detected <<<{COLOR_RESET}")
        time.sleep(0.4)
        print(f"{COLOR_CYAN}Resuming boot sequence...{COLOR_RESET}\n")
    
    # Phase 2: KERNEL INITIALIZATION
    print(f"\n{COLOR_WHITE}=== KERNEL INITIALIZATION ==={COLOR_RESET}")
    kernel_logs = [
        ("loading kernel modules...", "INFO", 0.2),
        ("mounting secure partitions...", "INFO", 0.3),
        ("entropy pool warming up...", "WARN", 0.4),
        ("initializing crypto engine (AES-256)...", "INFO", 0.5),
        ("verifying module signatures...", "INFO", 0.3),
    ]
    for msg, level, delay in kernel_logs:
        log(msg, level)
        time.sleep(delay)
    
    # Phase 3: NETWORK STACK INIT
    print(f"\n{COLOR_WHITE}=== NETWORK STACK INITIALIZATION ==={COLOR_RESET}")
    net_chain = [
        ("initializing network stack...", 0.2),
        ("probing network interfaces...", 0.3),
        ("dhcp request sent...", 0.5),
        ("dhcp ack received...", 0.2),
        ("ip assigned: [REDACTED]", 0.1),
        ("establishing encrypted tunnel...", 0.6),
        ("handshake with remote node...", 0.8),
        ("key exchange complete (ECDH)...", 0.3),
        ("session encrypted (AES-256-GCM)...", 0.2),
    ]
    for msg, delay in net_chain:
        log(msg, "INFO")
        time.sleep(delay)
    
    # Phase 4: SECURITY LAYER ACTIVATION with imperfect progress bars
    print(f"\n{COLOR_WHITE}=== SECURITY LAYER ACTIVATION ==={COLOR_RESET}")
    
    boot_logs = [
        ("locating strategic assets...", COLOR_GREEN),
        ("establishing encrypted uplink...", COLOR_GREEN),
        ("syncing global telemetry...", COLOR_GREEN),
        ("analyzing processor complex...", COLOR_YELLOW),
        ("initializing defense network...", COLOR_YELLOW),
        ("establishing satellite uplink...", COLOR_YELLOW),
        ("decrypting classified archives...", COLOR_RED),
        ("arming orbital strike platforms...", COLOR_RED),
        ("verifying launch codes...", COLOR_RED),
        ("activating shadow protocols...", BG_RED + COLOR_WHITE),
        ("engaging counter-intelligence...", BG_RED + COLOR_WHITE),
    ]
    
    for msg, color in boot_logs:
        padded_msg = f"{msg:<38}"  # Fixed width for alignment
        sys.stdout.write(f"{COLOR_CYAN}> {padded_msg}{COLOR_RESET}")
        sys.stdout.flush()
        
        # Imperfect progress
        progress = 0
        last_displayed = -1
        while progress < 100:
            step = random.choice([1, 2, 3, 5, 8, 13, 2, 3, 1, 5])  # Fibonacci-ish for realism
            
            # Occasional stall
            if random.random() < 0.08:
                time.sleep(random.uniform(0.2, 0.6))
            
            # Occasional retry
            if random.random() < 0.05:
                print(f"\n{COLOR_YELLOW}  ...retrying handshake...{COLOR_RESET}")
                time.sleep(0.4)
            
            progress = min(100, progress + step)
            
            # Only update display every ~10%
            if progress - last_displayed >= 10 or progress >= 100:
                bar_len = 20
                filled = int(progress / 100 * bar_len)
                bar = "█" * filled + "░" * (bar_len - filled)
                if progress < 30:
                    bar_col = COLOR_RED
                elif progress < 70:
                    bar_col = COLOR_YELLOW
                else:
                    bar_col = COLOR_GREEN
                sys.stdout.write(f"\r{COLOR_CYAN}> {padded_msg} [{bar_col}{bar}{COLOR_CYAN}] {bar_col}{progress}%{COLOR_RESET}")
                sys.stdout.flush()
                last_displayed = progress
            
            time.sleep(random.uniform(0.03, 0.12))
        
        # Final state
        final_bar = f"{COLOR_GREEN}{'█'*20}{COLOR_RESET}"
        print(f"\r{COLOR_CYAN}> {color}{padded_msg}{COLOR_RESET} [{final_bar}]")
        
        # CPU/MEM display occasionally
        if random.random() < 0.3:
            cpu = random.randint(15, 85)
            mem = random.randint(2048, 28000)
            sys.stdout.write(f"{COLOR_CYAN}  CPU: {cpu}% | MEM: {mem}MB{COLOR_RESET}\n")
        
        if "shadow" in msg.lower() or "counter" in msg.lower():
            print(f"{BG_RED}{COLOR_WHITE}{'  ⚠  WARNING: LETHAL SYSTEMS NOW ACTIVE  ⚠'}{COLOR_RESET}")
            time.sleep(0.4)
        else:
            time.sleep(random.uniform(0.1, 0.3))
    
    # Boot summary
    boot_time = round(time.time() - start_time, 2)
    print(f"\n{COLOR_GREEN}[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] [OK]   SYSTEM BOOT COMPLETE IN {boot_time}s{COLOR_RESET}")
    
    # Update nuclear weapons database with real-time data
    update_nuclear_weapons_database()
    
    print(f"{BG_RED}{COLOR_WHITE}{'>>> ALL SYSTEMS ARMED - AWAITING COMMAND <<<':^80}{COLOR_RESET}\n")
    time.sleep(1.0)
    clear_screen()

def display_disclaimer():
    clear_screen()
    print(COLOR_RED)
    banner_top = [f"{'██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗ ':^80}", f"{'██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝ ':^80}", f"{'██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗':^80}", f"{'██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║':^80}", f"{'╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝':^80}", f"{' ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ':^80}"]
    for line in banner_top: print(line)
    print(COLOR_RESET + COLOR_RED + "="*80)
    print(f"{COLOR_WHITE}{'STRATEGIC DEFENSE NETWORK - TERMINAL AUTHORITY: CLEARANCE REQUIRED':^80}{COLOR_RESET}")
    print(f"{COLOR_RED}{'='*80}{COLOR_RESET}")
    print("="*80)
    msgs = ["WARNING: W.O.L.F. CORPORATION PRIVATE NETWORK. UNAUTHORIZED ACCESS STRICTLY PROHIBITED.", "UNAUTHORISED PERSONNEL WILL RESULT IN IMMEDIATE TERMINATION OF EMPLOYMENT AND ASSET SEIZURE.", "CORPORATE SECURITY IS ARMED AND AUTHORIZED TO USE LETHAL FORCE IF REQUIRED.", "VIOLATORS WILL BE PURSUED TO THE FULL EXTENT OF CORPORATE AUTHORITY."]
    for l in msgs:
        if "WARNING" in l or "OFFENSE" in l: print(f"{BG_RED}{COLOR_WHITE}{l:^80}{COLOR_RESET}")
        else: print(f"{COLOR_RED}{l:^80}{COLOR_RESET}")
        time.sleep(0.3)
    print("\n" + f"{COLOR_YELLOW}{'ARE YOU AN AUTHORIZED OPERATOR? (Y/N)':^80}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush()
    if input().strip().upper() != "Y":
        clear_screen()
        for _ in range(3):
            print(f"{BG_RED}{' '*80}{COLOR_RESET}")
            time.sleep(0.1)
            clear_screen()
            time.sleep(0.1)
        skull_art = [
            f"{COLOR_RED}    ██╗ ███╗   ██╗ ████████╗ ██████╗  ██╗   ██╗ ██████╗  ███████╗ ██████╗     {COLOR_RESET}",
            f"{COLOR_RED}    ██║ ████╗  ██║ ╚══██╔══╝ ██╔══██╗ ██║   ██║ ██╔══██╗ ██╔════╝ ██╔══██╗    {COLOR_RESET}",
            f"{COLOR_RED}    ██║ ██╔██╗ ██║    ██║    ██████╔╝ ██║   ██║ ██║  ██║ █████╗   ██████╔╝    {COLOR_RESET}",
            f"{COLOR_RED}    ██║ ██║╚██╗██║    ██║    ██╔══██╗ ██║   ██║ ██║  ██║ ██╔══╝   ██╔══██╗    {COLOR_RESET}",
            f"{COLOR_RED}    ██║ ██║ ╚████║    ██║    ██║  ██║ ╚██████╔╝ ██████╔╝ ███████╗ ██║  ██║    {COLOR_RESET}",
            f"{COLOR_RED}    ╚═╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═╝    {COLOR_RESET}",
            "",
            f"{BG_RED}{COLOR_WHITE}{'⚠ UNAUTHORIZED BREACH DETECTED ⚠':^80}{COLOR_RESET}",
            "",
            f"{COLOR_RED}{'SYSTEM LOCKDOWN INITIATED...'}{COLOR_RESET}",
            f"{COLOR_RED}{'TRACING UPLINK SOURCE...'}{COLOR_RESET}",
            f"{COLOR_RED}{'DEPLOYING COUNTERMEASURES...'}{COLOR_RESET}",
            f"{COLOR_RED}{'TERMINAL ACCESS REVOKED'}{COLOR_RESET}",
            "",
            f"{BG_RED}{COLOR_WHITE}{' ☠ !!! BREACH PROTOCOLS INITIATED !!! ☠ '}{COLOR_RESET}"
        ]
        for line in skull_art:
            print(line)
            time.sleep(0.2)
        time.sleep(3)
        sys.exit(0)
    print(f"\n{COLOR_RED}{'>>> CLEARANCE ACKNOWLEDGED. PROCEEDING TO PRIMARY CORE. <<<'}"); time.sleep(1.0)

def login_screen():
    attempts = 0
    while attempts < 2:
        clear_screen()
        print(f"{COLOR_RED}╔{'═'*78}╗")
        print(f"║ {' ':^76} ║")
        print(f"║ {'           ██╗    ██╗  ██████╗  ██╗      ███████╗          ':^76} ║")
        print(f"║ {'           ██║    ██║ ██╔═══██╗ ██║      ██╔════╝          ':^76} ║")
        print(f"║ {'           ██║ █╗ ██║ ██║   ██║ ██║      █████╗            ':^76} ║")
        print(f"║ {'           ██║███╗██║ ██║   ██║ ██║      ██╔══╝            ':^76} ║")
        print(f"║ {'           ╚███╔███╔╝ ╚██████╔╝ ███████╗ ██║               ':^76} ║")
        print(f"║ {'            ╚══╝╚══╝   ╚═════╝  ╚══════╝ ╚═╝               ':^76} ║")
        print(f"║ {' ':^76} ║")
        print(f"║ {'W.O.L.F. CORPORATION - SECURE GATEWAY':^76} ║")
        print(f"║ {'TOP SECRET ACCESS - OMEGA CLEARANCE REQUIRED':^76} ║")
        print(f"╚{'═'*78}╝{COLOR_RESET}")
        print(f"{COLOR_YELLOW}{'OPERATOR ID:'}")
        sys.stdout.write(COLOR_BLUE); sys.stdout.flush(); uid = input().strip()
        print(f"\n{COLOR_YELLOW}{'AUTHENTICATION STRING:'}")
        sys.stdout.write(COLOR_GREEN); sys.stdout.flush(); pwd = get_blind_input()
        if uid == "MR_WOLF" and pwd == "WOLF!(@)":
            type_text(f"{COLOR_GREEN}AUTHENTICATION VERIFIED. SESSION ACTIVE.{COLOR_RESET}"); return True
        attempts += 1; type_text(f"{COLOR_RED}DISCREPANCY DETECTED. ATTEMPT {attempts}/2.{COLOR_RESET}"); time.sleep(1.5)
    return False

def nuclear_protocols_sequence(weapon_data=None, target_cont=None):
    clear_screen(); print(COLOR_RED)
    banner_sas = [" ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄ ", "▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌", "▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ", "▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌▐░▌    ▐░▌▐░▌          ", "▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ", "▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌", " ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█▀▀▀▀ ▐░█▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌   ▐░▌ ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌", "          ▐░▌▐░▌     ▀█▄  ▐░▌       ▐░▌▐░▌          ▐░▌    ▐░▌▐░▌          ▐░▌", " ▄▄▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌     ▐░█░▌ ▄▄▄▄▄▄▄█░▌", "▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌", " ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀ "]
    for line in banner_sas: print(line)
    print(f"\n{'STRATEGIC LAUNCH AUTHORIZATION PROTOCOLS'}\n{'='*80}{COLOR_RESET}")
    
    shared_seed = get_shared_seed()
    alpha_code, bravo_code, time_left = get_dynamic_codes()
    
    # Show expected codes for validation (codes come from WOLF_DECODER)
    print(f"\n{COLOR_YELLOW}{'*** CODE VALIDATION MODE ***':^80}")
    print(f"{COLOR_YELLOW}{'Enter codes from WOLF_DECODER for authorization':^80}")
    print(f"{COLOR_WHITE}{'Expected Codes:':^80}")
    print(f"{COLOR_GREEN}{'ALPHA: ' + alpha_code:^80}")
    print(f"{COLOR_YELLOW}{'BRAVO: ' + bravo_code:^80}")
    print(f"{COLOR_DIM}{'Time Remaining: ' + str(time_left) + ' seconds':^80}")
    time.sleep(3)
    
    phases = [
        ("ALPHA", alpha_code, "CODE IDENTIFICATION", "/// I \\\\", [
            " █████╗  ██╗      ██████╗  ██╗  ██╗  █████╗ ",
            "██╔══██╗ ██║      ██╔══██╗ ██║  ██║ ██╔══██╗",
            "███████║ ██║      ██████╔╝ ███████║ ███████║",
            "██╔══██║ ██║      ██╔═══╝  ██╔══██║ ██╔══██║",
            "██║  ██║ ███████╗ ██║      ██║  ██║ ██║  ██║",
            "╚═╝  ╚═╝  ╚═════╝ ╚═╝      ╚═╝  ╚═╝ ╚═╝  ╚═╝"
        ]),
        ("BRAVO", bravo_code, "LAUNCH CONFIRMATION", "/// II \\\\", [
            "██████╗  ██████╗   █████╗  ██║       ██║  ██████╗      ",
            "██╔══██║ ██╔══██╗ ██╔══██╗  ██║     ██╔╝ ██╔═══██║     ",
            "██████╔╝ ██████╔╝ ███████║   ██    ██╔╝  ██║   ██║     ",
            "██╔══██║ ██╔══██╗ ██╔══██║    ██  ██╔╝   ██║   ██║     ",
            "██████╔╝ ██║  ██║ ██╔══██║      ██╔═╝    ╚██████╔╝     ",     
            " ╚════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝      ╚═╝        ╚════╝      "
        ]),
        ("CHARLIE", "FINAL", "TERMINATION AUTHORIZATION", "/// III \\\\", [
            "██████╗  ██╗  ██╗  █████╗  ██████╗  ██╗      ██╗ ███████╗       ",
            "██╔══██╗ ██║  ██║ ██╔══██╗ ██╔══██╗ ██║      ██║ ██╔════╝       ",
            "██║  ╚═╝ ███████║ ███████║ ██████╔╝ ██║      ██║ █████╗         ",
            "██║  ██╗ ██╔══██║ ██╔══██║ ██╔══██╗ ██║      ██║ ██╔══╝         ",
            "██████╔╝ ██║  ██║ ██║  ██║ ██║  ██║ ███████╗ ██║ ███████╗       ",
            "╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝ ╚══════╝       "
        ])
    ]
    
    for phase_name, code, desc, symbol, art in phases:
        clear_screen()
        print(COLOR_RED + symbol + COLOR_RESET)
        print(f"{COLOR_YELLOW}{'='*80}")
        print(f"{COLOR_RED}{phase_name} PHASE - {desc}{COLOR_RESET}")
        print(f"AUTHORIZATION CODE: {COLOR_WHITE}{code}{COLOR_RESET}")
        print(f"{'='*80}{COLOR_RESET}")
        for line in art:
            print(f"{COLOR_RED}{line}{COLOR_RESET}")
        
        if phase_name == "ALPHA":
            print(f"\n{COLOR_WHITE}ENTER ALPHA AUTHORIZATION CODE:{COLOR_RESET}")
            sys.stdout.write(COLOR_RED); sys.stdout.flush()
            if input().strip().upper() != code:
                breach_protocol_initiated()
                return False
            type_text(f"\n{COLOR_GREEN}>>> ALPHA AUTHORIZATION ACCEPTED <<<{COLOR_RESET}", 0.01, 0.03)
            time.sleep(0.5)
        elif phase_name == "BRAVO":
            print(f"\n{COLOR_WHITE}ENTER BRAVO AUTHORIZATION CODE:{COLOR_RESET}")
            sys.stdout.write(COLOR_RED); sys.stdout.flush()
            if input().strip().upper() != code:
                breach_protocol_initiated()
                return False
            type_text(f"\n{COLOR_GREEN}>>> BRAVO AUTHORIZATION ACCEPTED <<<{COLOR_RESET}", 0.01, 0.03)
            time.sleep(0.5)
        elif phase_name == "CHARLIE":
            print(f"\n{BG_RED}{COLOR_WHITE} !!! FINAL EXECUTION WARNING !!! {COLOR_RESET}")
            print(f"{COLOR_RED}ALL RESTRAINT BYPASSED. TARGETS TO BE LOCKED AND READY FOR LAUNCH.{COLOR_RESET}")
            print(f"\n{COLOR_WHITE}PROCEED WITH FINAL EXECUTION? (YES/NO):{COLOR_RESET}")
            sys.stdout.write(COLOR_RED); sys.stdout.flush()
            if input().strip().upper() != "YES":
                breach_protocol_initiated()
                return False
            
            # COUNTDOWN SEQUENCE
            type_text(f"\n{COLOR_YELLOW}{'='*80}", 0.05, 0.1)
            print(f"{COLOR_RED}{'    ╔════════════════════════════════════════════════════════════╗':^80}")
            print(f"{COLOR_RED}{'    ║  COUNTDOWN TO IMPACT                                       ║':^80}")
            print(f"{COLOR_RED}{'    ║                                                            ║':^80}")
            print(f"{COLOR_RED}{'    ║  T-MINUS 00:00:00                                          ║':^80}")
            print(f"{COLOR_RED}{'    ╚════════════════════════════════════════════════════════════╝':^80}")
            time.sleep(1)
            
            # Countdown animation
            for t in range(30, -1, -1):
                time.sleep(1)
                # Clear entire screen area and print single countdown box
                print(f"\033[2J\033[H", end="")  # Clear screen and move cursor to top
                print(f"{COLOR_RED}    ╔════════════════════════════════════════════════════════════╗")
                print(f"{COLOR_RED}    ║  COUNTDOWN TO IMPACT                                       ║")
                print(f"{COLOR_RED}    ║                                                            ║")
                print(f"{COLOR_RED}    ║  T-MINUS {t:02d}:00                                        ║")
                print(f"{COLOR_RED}    ╚════════════════════════════════════════════════════════════╝")
                sys.stdout.flush()
            
            print()  # Clear the line after countdown
            time.sleep(1)
            
            # LAUNCH SEQUENCE
            type_text(f"\n{COLOR_YELLOW}{'='*80}", 0.05, 0.1)
            print(f"{COLOR_RED}{'    ╔══════════════════════════════════════════════════════════╗':^80}")
            print(f"{COLOR_RED}{'    ║  LAUNCH SEQUENCE INITIATED                               ║':^80}")
            print(f"{COLOR_RED}{'    ║                                                          ║':^80}")
            print(f"{COLOR_RED}{'    ║  STAGE 1: IGNITION PRIMARY BOOSTER - NOMINAL             ║':^80}")
            print(f"{COLOR_RED}{'    ║  STAGE 2: SECONDARY BOOSTER IGNITION - NOMINAL           ║':^80}")
            print(f"{COLOR_RED}{'    ║  STAGE 3: WARHEAD SEPARATION - CONFIRMED                 ║':^80}")
            print(f"{COLOR_RED}{'    ║  STAGE 4: RE-ENTRY VEHICLE ACTIVATION - NOMINAL          ║':^80}")
            print(f"{COLOR_RED}{'    ║  STAGE 5: FINAL APPROACH VECTOR - CALCULATED             ║':^80}")
            print(f"{COLOR_RED}{'    ║  TARGET LOCK: ACHIEVED - PRECISION STRIKE IMMINENT       ║':^80}")
            print(f"{COLOR_RED}{'    ╚══════════════════════════════════════════════════════════╝':^80}")
            time.sleep(2)
            
            # Launch details based on weapon type
            if isinstance(weapon_data, tuple):
                # SLBM (Submarine-Launched Ballistic Missile)
                missile, vessel, location, coords = weapon_data
                print(f"\n{COLOR_CYAN}>>> LAUNCH CONFIRMED: {missile.upper()} FROM {vessel.upper()} <<<{COLOR_RESET}")
                print(f"{COLOR_CYAN}>>> SUBMARINE DEPTH: {location.upper()} <<<{COLOR_RESET}")
                print(f"{COLOR_CYAN}>>> TARGET COORDINATES: {coords.upper()} <<<{COLOR_RESET}")
                print(f"\n{COLOR_WHITE}MESSAGE FROM CAPTAIN OF {vessel.upper()}:")
                
                # Personalized vessel and missile Data
                vessel_data = {
                    "USS NEBRASKA": "Ohio-class ballistic missile submarine, operating at test depth 150m",
                    "USS TENNESSEE": "Ohio-class SSBN, Pacific Fleet strategic deterrent",
                    "USS PENNSYLVANIA": "Ohio-class submarine, Atlantic patrol, 24 Trident II missiles",
                    "USS LOUISIANA": "Ohio-class SSBN, equipped with Mk4 re-entry systems",
                    "USS GEORGIA": "Ohio-class submarine, recently retrofitted with advanced targeting",
                    "USS HENRY M JACKSON": "Virginia-class fast attack sub, special operations capable",
                    "USS SOUTH DAKOTA": "Ohio-class SSBN, strategic missile deployment platform",
                    "USS MARYLAND": "Ohio-class submarine, Atlantic strategic presence",
                    "USS WYOMING": "Ohio-class SSBN, Pacific theater operations",
                    "USS ALABAMA": "Ohio-class submarine, Arctic deployment specialist",
                    "USS RHODE ISLAND": "Ohio-class SSBN, Eastern Atlantic strategic coverage"
                }
                
                missile_data = {
                    "USS NEBRASKA": "Trident II D5LE, MIRV system with 8 W88 warheads (475 kt each)",
                    "USS TENNESSEE": "Trident II D5, upgraded guidance systems, enhanced penetration capability",
                    "USS PENNSYLVANIA": "Trident II D5, nuclear deterrent with advanced countermeasures",
                    "USS LOUISIANA": "Trident II D5LE, multiple independent targeting capability",
                    "USS GEORGIA": "Trident II D5, state-of-the-art navigation and targeting",
                    "USS HENRY M JACKSON": "Trident II D5, special operations with enhanced stealth",
                    "USS SOUTH DAKOTA": "Trident II D5, strategic strike platform with extended range",
                    "USS MARYLAND": "Trident II D5, rapid deployment capability",
                    "USS WYOMING": "Trident II D5, Pacific strategic missile system",
                    "USS ALABAMA": "Trident II D5, Arctic warfare specialist",
                    "USS RHODE ISLAND": "Trident II D5, Atlantic strategic missile platform"
                }
                
                # Display vessel and Missile Information
                print(f"{COLOR_YELLOW}    'Vessel Status: {vessel_data.get(vessel.upper(), 'Classified submarine operating at strategic depth')}'")
                print(f"{COLOR_YELLOW}    'Missile System: {missile_data.get(missile.upper(), 'Classified strategic missile system')}'")
                print(f"{COLOR_YELLOW}    'Current Depth: {location.upper()} meters beneath surface'")
                print(f"{COLOR_YELLOW}    'Seal hatches open. Missile tube pressurization complete.'")
                print(f"{COLOR_YELLOW}    'Primary ignition sequence initiated. All systems nominal.'")
                print(f"{COLOR_YELLOW}    'Submarine breaking surface. Ejecting water from missile tube.'")
                print(f"{COLOR_YELLOW}    'SLBM cleared surface. Vertical ascent confirmed.'")
                print(f"{COLOR_YELLOW}    'First stage separation successful. Trajectory locked.'")
                print(f"{COLOR_YELLOW}    'Target acquisition confirmed. Final approach vector calculated.'")
                print(f"{COLOR_YELLOW}    'Awaiting strategic command confirmation for terminal phase.'")
            else:
                # ICBM (Intercontinental Ballistic Missile)
                weapon_name = weapon_data
                print(f"\n{COLOR_CYAN}>>> LAUNCH CONFIRMED: {weapon_name.upper()} FROM SILO-BASED FACILITY <<<{COLOR_RESET}")
                print(f"{COLOR_CYAN}>>> TARGET LOCK: {target_cont.upper()} <<<{COLOR_RESET}")
                print(f"{COLOR_CYAN}>>> PAYLOAD: THERMONUCLEAR MIRV SYSTEM <<<{COLOR_RESET}")
                print(f"\n{COLOR_WHITE}MESSAGE FROM OFFICER-IN-CHARGE AT ICBM CENTRE:")
                
                # Use global nuclear weapons database updated during bootup
                global icbm_data, slbm_data
                
                # Vessel/Location Status System
                import random
                status_options = ["NADA", "MEH", "WILCO"]
                status_colors = {"NADA": COLOR_RED, "MEH": COLOR_YELLOW, "WILCO": COLOR_GREEN}
                
                # Country-specific vessel/location data
                vessel_status = {
                    # UNITED STATES - ICBMs
                    "LGM-30G MINUTEMAN III": f"F.E. Warren AFB, Montana - Status: {random.choice(status_options)}",
                    "LGM-30G MINUTEMAN": f"F.E. Warren AFB, Montana - Status: {random.choice(status_options)}",
                    "LGM-118A PEACEKEEPER": f"F.E. Warren AFB, Montana - Status: {random.choice(status_options)}",
                    "MX MISSILE": f"Utah/Wyoming silos - Status: {random.choice(status_options)}",
                    "MINUTEMAN III": f"F.E. Warren AFB, Montana - Status: {random.choice(status_options)}",
                    "TITAN II": f"Vandenberg AFB, California - Status: {random.choice(status_options)}",
                    
                    # UNITED STATES - SLBMs
                    "UGM-133A TRIDENT II D5": f"USS Nebraska, Ohio-class SSBN - Status: {random.choice(status_options)}",
                    "UGM-133A TRIDENT II": f"USS Tennessee, Ohio-class SSBN - Status: {random.choice(status_options)}",
                    
                    # RUSSIA - ICBMs
                    "RS-28 SARMAT": f"Saratov region, silos - Status: {random.choice(status_options)}",
                    "RS-24 YARS": f"Mobile launchers across Russia - Status: {random.choice(status_options)}",
                    "RT-2PM2 TOPOL-M": f"Siberia mobile launchers - Status: {random.choice(status_options)}",
                    "R-36M2 VOEVODA": f"Uzhur missile division - Status: {random.choice(status_options)}",
                    "UR-100N STILETTO": f"Kozelsk missile base - Status: {random.choice(status_options)}",
                    "RS-24": f"Mobile launchers across Russia - Status: {random.choice(status_options)}",
                    
                    # RUSSIA - SLBMs
                    "RSM-56 BULAVA": f"Yury Dolgoruky, Borei-class SSBN - Status: {random.choice(status_options)}",
                    "R-29RMU SINEVA": f"K-114 Tula, Delta IV-class SSBN - Status: {random.choice(status_options)}",
                    "R-29RMU2 LAYNER": f"K-117 Bryansk, Delta IV-class SSBN - Status: {random.choice(status_options)}",
                    
                    # CHINA - ICBMs
                    "DF-5B": f"Central China, 12 silo complexes - Status: {random.choice(status_options)}",
                    "DF-31A": f"Northeastern China, mobile sites - Status: {random.choice(status_options)}",
                    "DF-31AG": f"Eastern China, advanced sites - Status: {random.choice(status_options)}",
                    "DF-41": f"Central China, 12 silo complexes - Status: {random.choice(status_options)}",
                    "DF-31": f"Northeastern China, mobile sites - Status: {random.choice(status_options)}",
                    "DONGFENG 5": f"Central China, mobile launchers - Status: {random.choice(status_options)}",
                    "DF-5": f"Central China, mobile launchers - Status: {random.choice(status_options)}",
                    
                    # CHINA - SLBMs
                    "JL-2": f"Type 094 SSBN, South China Sea - Status: {random.choice(status_options)}",
                    "JL-3": f"Type 096 SSBN, newer deployment - Status: {random.choice(status_options)}",
                    
                    # FRANCE - SLBMs (no ICBMs)
                    "M51.2": f"Le Triomphant-class SSBN - Status: {random.choice(status_options)}",
                    "M51.3": f"Le Terrible-class SSBN - Status: {random.choice(status_options)}",
                    "M-51 HADES": f"French Navy submarines - Status: {random.choice(status_options)}",
                    
                    # UK - SLBMs (no ICBMs)
                    "UGM-133A TRIDENT II D5 UK": f"HMS Vanguard, Vanguard-class SSBN - Status: {random.choice(status_options)}",
                    "UGM-27 POLARIS": f"Royal Navy submarines - Status: {random.choice(status_options)}",
                    
                    # INDIA - ICBMs
                    "AGNI-V": f"Mobile launchers across India - Status: {random.choice(status_options)}",
                    "PRITHVI": f"Rail-mobile systems - Status: {random.choice(status_options)}",
                    "K-4": f"Mobile launch sites - Status: {random.choice(status_options)}",
                    
                    # INDIA - SLBMs
                    "K-4": f"INS Arihant, Arihant-class SSBN - Status: {random.choice(status_options)}",
                    "K-15": f"INS Arighat, Arihant-class SSBN - Status: {random.choice(status_options)}",
                    
                    # PAKISTAN - ICBMs (no SLBMs)
                    "SHAHEEN-III": f"Road-mobile launchers - Status: {random.choice(status_options)}",
                    "GHORI-III": f"Road-mobile launchers - Status: {random.choice(status_options)}",
                    
                    # NORTH KOREA - ICBMs (no SLBMs)
                    "HWASONG-14": f"Underground facilities - Status: {random.choice(status_options)}",
                    "HWASONG-15": f"Underground facilities - Status: {random.choice(status_options)}",
                    "HWASONG-17": f"Underground facilities - Status: {random.choice(status_options)}",
                    "Hwasong-15": f"Underground facilities - Status: {random.choice(status_options)}",
                    "Hwasong-12": f"Underground facilities - Status: {random.choice(status_options)}",
                    
                    # ISRAEL - ICBMs (no SLBMs)
                    "JERICHO-III": f"Mobile launch sites - Status: {random.choice(status_options)}",
                    "JERICHO-2": f"Mobile launch sites - Status: {random.choice(status_options)}"
                }
                
                silo_data = {
                    "LGM-30G MINUTEMAN": "F.E. Warren AFB, Montana - 50 silos operational",
                    "LGM-118A PEACEKEEPER": "F.E. Warren AFB, Montana - 200 silos under construction",
                    "MX MISSILE": "Multiple sites across Utah, Wyoming, Nebraska, Colorado - 47 super-hardened silos",
                    "RS-28 SARMAT": "Saratov region, 5 major silo complexes underground",
                    "RT-2PM2 TOPOL-M": "Mobile launchers across Siberia, road-mobile capability",
                    "DF-41": "Central China, 12 fixed silo complexes with underground facilities",
                    "DF-31": "Northeastern China, 6 mobile launch sites with rail deployment",
                    "DONGFENG 5": "Central China, mobile launchers with rapid deployment capability"
                }
                
                # Display ICBM System and Warhead Information
                print(f"{COLOR_YELLOW}    'ICBM System: {icbm_data.get(weapon_name.upper(), 'Classified strategic missile system')}'")
                print(f"{COLOR_YELLOW}    'Warhead Configuration: {warhead_data.get(weapon_name.upper(), 'Classified thermonuclear warhead system')}'")
                print(f"{COLOR_YELLOW}    'Launch Facility: {vessel_status.get(weapon_name.upper(), 'Classified strategic launch facility')}'")
                print(f"{COLOR_YELLOW}    'Target Continent: {target_cont.upper()} theater of operations'")
                print(f"{COLOR_YELLOW}    'Launch sequence executed. All systems operational.'")
                print(f"{COLOR_YELLOW}    'Warhead armed and deployed. Trajectory optimized.'")
                print(f"{COLOR_YELLOW}    'Multiple Independent Re-entry Vehicle systems active.'")
                print(f"{COLOR_YELLOW}    'Target destruction imminent. God have mercy on our souls.'")
            
            type_text(f"\n{COLOR_RED}>>> AUTHORIZATION SUCCESSFUL. COMMENCING IGNITION. <<<{COLOR_RESET}", 0.01, 0.03)
            return True
    return True

def run_war_scenario(initiating_nation: str, data_mgr: DataManager, weapon_data):
    # Extract weapon name from tuple if SLBM, or use directly if ICBM
    if isinstance(weapon_data, tuple):
        weapon_name = weapon_data[0]  # SLBM: (missile, vessel, location, coords)
        vessel_info = weapon_data[1] if len(weapon_data) > 1 else "UNKNOWN"
        location_info = weapon_data[2] if len(weapon_data) > 2 else "UNKNOWN"
        coords_info = weapon_data[3] if len(weapon_data) > 3 else "UNKNOWN"
    else:
        weapon_name = weapon_data  # ICBM: just the name
        vessel_info = "SILO-BASED"
        location_info = "LAND-BASED LAUNCH FACILITY"
        coords_info = "CLASSIFIED"
    
    clear_screen(); print(f"{COLOR_RED}*** GLOBAL THERMONUCLEAR WAR SCENARIO INITIALIZED ***{COLOR_RESET}\n")
    print(f"{COLOR_YELLOW}PAYLOAD DELIVERY: {weapon_name}{COLOR_RESET}")
    print(f"{COLOR_YELLOW}LAUNCH ORIGIN: {initiating_nation}{COLOR_RESET}")
    if vessel_info != "SILO-BASED":
        print(f"{COLOR_CYAN}PLATFORM: {vessel_info}{COLOR_RESET}")
        print(f"{COLOR_CYAN}LOCATION: {location_info}{COLOR_RESET}")
        print(f"{COLOR_CYAN}COORDS:   {coords_info}{COLOR_RESET}")
    
    conts = list(CONTINENT_MAPPING.keys())
    print(f"{COLOR_CYAN}>>> SELECT TARGET CONTINENT <<< {COLOR_RESET}")
    for i, c in enumerate(conts, 1): print(f"[{i}] {c}")
    
    print(f"\n{COLOR_WHITE}WHICH REGION SHALL BE TARGETED?: {COLOR_RESET}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush()
    c_choice = input().strip().upper()
    target_cont = conts[int(c_choice)-1] if c_choice.isdigit() and 1<=int(c_choice)<=len(conts) else "ASIA"
    
    # Nuclear Fallout Warning Logic
    origin_cont = get_nation_continent(initiating_nation)
    if origin_cont == target_cont:
        print(f"\n{BG_RED}{COLOR_WHITE} !!! WARNING: PROXIMITY HAZARD DETECTED !!! {COLOR_RESET}")
        print(f"{COLOR_RED}TARGETING SAME CONTINENT ({target_cont}).")
        print(f"HIGH RISK OF ATMOSPHERIC NUCLEAR FALLOUT DUE TO LOCAL WEATHER AND WIND PATTERNS.")
        print(f"CONTINUED OPERATIONS MAY CONTAMINATE LAUNCH ORIGIN.{COLOR_RESET}")
        print(f"\n{COLOR_YELLOW}DO YOU WISH TO PROCEED WITH THIS STRIKE? (YES/NO): {COLOR_RESET}")
        sys.stdout.write(COLOR_RED); sys.stdout.flush()
        if input().strip().upper() != "YES":
            breach_protocol_initiated()
            return

    countries = [c for c in CONTINENT_MAPPING.get(target_cont, []) if c.upper() in world_data.WORLD_DATA]
    print(f"\n{COLOR_CYAN}>>> SELECT TARGET NATION <<< {COLOR_RESET}")
    for i, n in enumerate(countries, 1): print(f"[{i}] {n}")
    
    print(f"\n{COLOR_WHITE}SELECT TARGET NATION ID: {COLOR_RESET}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush()
    n_choice = input().strip(); target_nation = countries[int(n_choice)-1] if n_choice.isdigit() and 1<=int(n_choice)<=len(countries) else countries[0]
    
    cities = data_mgr.get_cities_for_nation(target_nation)
    print(f"\n{COLOR_CYAN}>>> SELECT TARGET CITY <<< {COLOR_RESET}")
    print(f"{COLOR_DIM}{'ID':<6} {'CITY':<25} {'COORDINATES':<25} {'POPULATION':<15} {'ETA'}{COLOR_RESET}")
    for i, c in enumerate(cities[:20], 1):
        name, core, metro, eta, coords = c
        coord_str = f"{coords[0]:.2f}N, {coords[1]:.2f}E"
        print(f"[{i:<2}]  {name:<25} {coord_str:<25} {metro:<15,.0f} {eta}m")
        
    print(f"\n{COLOR_WHITE}SELECT TARGET ID: {COLOR_RESET}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush()
    city_id = input().strip(); target_city = cities[int(city_id)-1][0] if city_id.isdigit() and 1<=int(city_id)<=len(cities) else cities[0][0]
    
    if not nuclear_protocols_sequence(weapon_data, target_cont): return
    for i in range(5, 0, -1): print(f"LAUNCH IN T-MINUS {i}...", end="\r"); time.sleep(1)
    
    # Launch Success Notification
    clear_screen()
    print(f"{COLOR_GREEN}{'='*80}")
    print(f"{COLOR_GREEN}{'*** LAUNCH SUCCESSFUL ***':^80}")
    print(f"{COLOR_GREEN}{'='*80}")
    print(f"{COLOR_YELLOW}MISSILE STATUS: INBOUND TO TARGET")
    print(f"{COLOR_YELLOW}VELOCITY: MACH 23 - FINAL APPROACH")
    print(f"{COLOR_YELLOW}ETA TO TARGET: 25 MINUTES")
    time.sleep(2)
    
    # Detonation Notification
    clear_screen()
    print(f"{COLOR_RED}{'='*80}")
    print(f"{COLOR_RED}{'*** NUCLEAR DETONATION CONFIRMED ***':^80}")
    print(f"{COLOR_RED}{'='*80}")
    print(f"\n{COLOR_WHITE}WARHEAD DETONATED AT: {target_city.upper()}")
    print(f"{COLOR_WHITE}COORDINATES: {data_mgr.get_city_coordinates(target_city)[0]:.2f}N, {data_mgr.get_city_coordinates(target_city)[1]:.2f}E")
    print(f"{COLOR_WHITE}YIELD: {data_mgr.get_weapon_yield(weapon_name):,} KILOTONS")
    print(f"{COLOR_WHITE}BLAST RADIUS: {data_mgr.calculate_blast_radius(weapon_name):.1f} KILOMETERS")
    print(f"\n{COLOR_RED}THERMONUCLEAR EXPLOSION SUCCESSFUL")
    print(f"{COLOR_RED}TARGET COMPLETELY DESTROYED")
    time.sleep(3)
    
    type_text(f"\n{COLOR_RED}IMPACT CONFIRMED AT {target_city}.{COLOR_RESET}")
    print(f"ESTIMATED CASUALTIES: {data_mgr.calculate_casualties(target_city, weapon_name):,d}")
    time.sleep(2); clear_screen()
    print(f"{COLOR_RED}╔{'═'*58}╗")
    print(f"║ {'MISSION OBJECTIVE: SUCCESSFUL':^56} ║")
    print(f"╚{'═'*58}╝")
    print(f"SYSTEM STATE: DEFCON 5.{COLOR_RESET}")
    time.sleep(2); sys.exit(0)

def start_sync_server():
    """Start the code synchronization server"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 55555))
        server_socket.listen(5)
        
        print(f"{COLOR_GREEN}{'='*80}")
        print(f"{COLOR_GREEN}{'*** WOLF CODE SYNC SERVER STARTED ***':^80}")
        print(f"{COLOR_GREEN}{'='*80}")
        print(f"{COLOR_WHITE}Server listening on port 55555")
        print(f"{COLOR_CYAN}Waiting for decoder connections...")
        print(f"{COLOR_DIM}Press Ctrl+C to stop server{COLOR_RESET}")
        
        clients = []
        # Initialize with dummy codes so clients can connect immediately
        current_codes = ("ALPHA-INIT", "BRAVO-INIT")
        
        while True:
            try:
                client_socket, address = server_socket.accept()
                clients.append(client_socket)
                print(f"{COLOR_YELLOW}Decoder connected from {address[0]}:{address[1]}")
                
                # Send current codes to client
                if current_codes:
                    message = json.dumps({
                        'type': 'codes',
                        'alpha': current_codes[0],
                        'bravo': current_codes[1],
                        'timestamp': time_module.time()
                    })
                    client_socket.send(message.encode())
                    
                # Start client handler thread
                def handle_client(client_socket, address):
                    try:
                        while True:
                            data = client_socket.recv(1024).decode()
                            if data == 'ACK':
                                print(f"{COLOR_CYAN}Acknowledgment received from {address[0]}:{address[1]}")
                            time_module.sleep(1)
                    except:
                        pass
                    finally:
                        client_socket.close()
                        if client_socket in clients:
                            clients.remove(client_socket)
                
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                print(f"\n{COLOR_RED}Server shutting down...")
                break
            except Exception as e:
                print(f"{COLOR_RED}Server error: {e}")
                break
            finally:
                server_socket.close()
            
    except Exception as e:
        print(f"{COLOR_RED}Failed to start server: {e}")
    if os.name == 'nt' and ctypes:
        try: ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
        except: pass
    
    clear_screen()
    print(f"{COLOR_RED}{'='*80}")
    print(f"{COLOR_RED}{'*** WOLF NUCLEAR COMMAND SYSTEM ***':^80}")
    print(f"{COLOR_RED}{'='*80}")
    
    print(f"{COLOR_WHITE}Select mode:")
    print(f"{COLOR_GREEN}[1] SERVER - Host code synchronization")
    print(f"{COLOR_GREEN}[2] CLIENT - Receive synchronized codes") 
    print(f"{COLOR_GREEN}[3] NORMAL - Launch sequence")
    
    while True:
        print(f"\n{COLOR_WHITE}{'CHOICE: ':^80}", end="")
        sys.stdout.write(COLOR_WHITE)
        sys.stdout.flush()
        choice = input().strip()
        
        if choice == "1":
            start_sync_server()
        elif choice == "2":
            # Normal launch sequence
            system_boot_sequence()
            display_disclaimer()
            if not login_screen(): sys.exit(0)
            data_mgr = DataManager()
            engine = ScenarioEngine()
            clear_screen()
            main_menu_loop(data_mgr, engine)
        elif choice == "3":
            print(f"{COLOR_YELLOW}Exiting...")
            break
        else:
            print(f"{BG_RED}{COLOR_WHITE}{'INVALID CHOICE':^80}{COLOR_RESET}")
            time.sleep(1)

    wolf_banner = [
        f"{COLOR_RED}╔{'═'*84}╗",
        f"║ {'        ██╗    ██╗  ██████╗  ██╗      ███████╗        ':^82} ║",
        f"║ {'        ██║    ██║ ██╔═══██╗ ██║      ██╔════╝        ':^82} ║",
        f"║ {'        ██║ █╗ ██║ ██║   ██║ ██║      █████╗          ':^82} ║",
        f"║ {'        ██║███╗██║ ██║   ██║ ██║      ██╔══╝          ':^82} ║",
        f"║ {'        ╚███╔███╔╝ ╚██████╔╝ ███████╗ ██║             ':^82} ║",
        f"║ {'         ╚══╝╚══╝   ╚═════╝  ╚══════╝ ╚═╝             ':^82} ║",
        f"║ {'                                                            ':^82} ║",
        f"║ {'███████╗ ████████╗ ██████╗   █████╗  ████████╗ ███████╗  ██████╗  ██╗  ██████╗':^82} ║",
        f"║ {'██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔══██╗ ╚══██╔══╝ ██╔════╝ ██╔════╝  ██║ ██╔════╝':^82} ║",
        f"║ {'███████╗    ██║    ██████╔╝ ███████║    ██║    █████╗   ██║  ███╗ ██║ ██║     ':^82} ║",
        f"║ {'╚════██║    ██║    ██╔══██╗ ██╔══██║    ██║    ██╔══╝   ██║   ██║ ██║ ██║     ':^82} ║",
        f"║ {'███████║    ██║    ██║  ██║ ██║  ██║    ██║    ███████╗ ╚██████╔╝ ██║  ██████╗':^82} ║",
        f"║ {'╚══════╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═╝    ╚═╝    ╚══════╝  ╚═════╝  ╚═╝  ╚═════╝':^82} ║",
        f"╚{'═'*84}╝{COLOR_RESET}"
    ]
    for line in wolf_banner: print(line)
    print(f"\n{COLOR_YELLOW}{'SET GLOBAL DEFCON LEVEL (1-5):'}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush(); def_level = input().strip() or "5"
    defcon_digits = {
        "1": ["  ██╗  ", " ███║  ", " ╚██║  ", "  ██║  ", "  ██║  ", "  ╚═╝  "],
        "2": ["██████╗", "╚════██╗", " █████╔╝", "██╔═══╝ ", "███████╗", "╚══════╝"],
        "3": ["██████╗", "╚════██╗", " █████╔╝", " ╚═══██╗", "██████╔╝", "╚═════╝ "],
        "4": ["██╗  ██╗", "██║  ██║", "███████║", "╚═══██║", "    ██║", "    ╚═╝"],
        "5": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"]
    }
    digit_art = defcon_digits.get(def_level, defcon_digits["5"])
    
    clear_screen()
    print(f"{COLOR_RED}{COLOR_BLINK}╔{'═'*78}╗")
    warning_lines = [
        "██╗    ██╗  █████╗  ██████╗  ███╗   ██╗ ██╗ ███╗   ██╗  ██████╗ ",
        "██║    ██║ ██╔══██╗ ██╔══██╗ ████╗  ██║ ██║ ████╗  ██║ ██╔════╝ ",
        "██║ █╗ ██║ ███████║ ██████╔╝ ██╔██╗ ██║ ██║ ██╔██╗ ██║ ██║  ███╗",
        "██║███╗██║ ██╔══██║ ██╔══██╗ ██║╚██╗██║ ██║ ██║╚██╗██║ ██║   ██║",
        "╚███╔███╔╝ ██║  ██║ ██║  ██║ ██║ ╚████║ ██║ ██║ ╚████║ ╚██████╔╝",
        " ╚══╝╚══╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝  ╚═══╝  ╚═════╝"
    ]
    for line in warning_lines:
        print(f"║ {line:^76} ║")
    print(f"║ {' ':^76} ║")
    defcon_text = [
        " ██████╗ ███████╗███████╗ ██████╗  ██████╗  ███╗   ██╗",
        " ██╔══██╗██╔════╝██╔════╝██╔════╝ ██╔═══██╗ ████╗  ██║",
        " ██║  ██║█████╗  █████╗  ██║      ██║   ██║ ██╔██╗ ██║",
        " ██║  ██║██╔══╝  ██╔══╝  ██║      ██║   ██║ ██║╚██╗██║",
        " ██████╔╝███████╗██║     ╚██████╗ ╚██████╔╝ ██║ ╚████║",
        " ╚═════╝ ╚══════╝╚═╝      ╚═════╝  ╚═════╝  ╚═╝  ╚═══╝"
    ]
    for i in range(6):
        line_content = f"{defcon_text[i]}   {digit_art[i]}"
        print(f"║ {line_content:^76} ║")
    print(f"║ {' ':^76} ║")
    print(f"║ {'DEFCON LEVEL ' + def_level:^76} ║")
    print(f"║ {'WARNING: NUCLEAR PROTOCOLS ACTIVE. AUTHORIZED PERSONNEL ONLY.':^76} ║")
    print(f"╚{'═'*78}╝{COLOR_RESET}")
    time.sleep(1.5)
    nuclear_nations = ["UNITED STATES", "RUSSIA", "CHINA", "UK", "FRANCE", "INDIA", "PAKISTAN", "NORTH KOREA", "ISRAEL"]
    print(f"\n{COLOR_GREEN}{'>>> SELECT INITIATING NATION <<< '}")
    for i, n in enumerate(nuclear_nations, 1): print(f"[{i}] {n}")
    print(f"\n{COLOR_WHITE}{'COMMAND>'}")
    sys.stdout.write(COLOR_RED); sys.stdout.flush()
    n_in = input().strip(); init_nation = nuclear_nations[int(n_in)-1] if n_in.isdigit() and 1<=int(n_in)<=9 else "UNITED STATES"
    print(f"\n{COLOR_RED}╔{'═'*78}╗")
    print(f"║ {BG_RED}{COLOR_WHITE}{init_nation}{COLOR_RESET}{COLOR_RED}{' '*(76-len(init_nation))} ║")
    unlocked_art = [
        "                                                                    ",
        "██╗   ██╗ ███╗   ██╗ ██╗       ██████╗   ██████╗ ██╗  ██╗ ███████╗ ██████╗ ",
        "██║   ██║ ████╗  ██║ ██║      ██╔═══██╗ ██╔════╝ ██║ ██╔╝ ██╔════╝ ██╔══██╗",
        "██║   ██║ ██╔██╗ ██║ ██║      ██║   ██║ ██║      █████╔╝  █████╗   ██║  ██║",
        "██║   ██║ ██║╚██╗██║ ██║      ██║   ██║ ██║      ██╔═██╗  ██╔══╝   ██║  ██║",
        "╚██████╔╝ ██║ ╚████║ ███████╗ ╚██████╔╝ ╚██████╗ ██║  ██╗ ███████╗ ██████╔╝",
        " ╚═════╝  ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝   ╚═════╝ ╚═╝  ╚═╝ ╚══════╝ ╚═════╝ "
    ]
    for line in unlocked_art:
        print(f"║ {line:<76} ║")
    print(f"║ {' '*(76-len('NUCLEAR ASSETS ACTIVATED'))}{BG_RED}{COLOR_WHITE}NUCLEAR ASSETS ACTIVATED{COLOR_RESET}{COLOR_RED} ║")
    print(f"╚{'═'*78}╝{COLOR_RESET}")
    weapons_map = {
        "UNITED STATES": {
            "ICBM": ["LGM-30G MINUTEMAN III"],
            "SLBM": [
                ("UGM-133 TRIDENT II", "USS Henry M. Jackson (SSBN-730)", "Naval Base Kitsap-Bangor, WA, USA", "47.7256°N, 122.7152°W"),
                ("UGM-133 TRIDENT II", "USS West Virginia (SSBN-736)", "Naval Submarine Base Kings Bay, GA, USA", "30.7889°N, 81.5554°W")
            ]
        },
        "RUSSIA": {
            "ICBM": ["RS-28 SARMAT", "RT-2PM2 TOPOL-M"],
            "SLBM": [
                ("RSM-56 BULAVA", "K-551 Vladimir Monomakh (Borei-class)", "Gadzhiyevo Naval Base, Murmansk Oblast", "69.2667°N, 33.4833°E"),
                ("R-29RMU2 LAYNER", "K-114 Tula (Delta IV-class)", "Gadzhiyevo Naval Base, Murmansk Oblast", "69.2667°N, 33.4833°E")
            ]
        },
        "CHINA": {
            "ICBM": ["DF-41", "DF-31AG"],
            "SLBM": [
                ("JL-3", "Jin-class SSBN (Type 094)", "Yulin Naval Base, Hainan", "18.2333°N, 109.6167°E"),
                ("JL-2", "Jin-class SSBN (Type 094)", "Jianggezhuang Submarine Base, Shandong", "36.2333°N, 120.4833°E")
            ]
        },
        "UK": {
            "ICBM": [],
            "SLBM": [
                ("UGM-133 TRIDENT II", "HMS Vanguard (S28)", "HMNB Clyde (Faslane), Scotland", "56.0333°N, 4.8167°W"),
                ("UGM-133 TRIDENT II", "HMS Victorious (S29)", "HMNB Clyde (Faslane), Scotland", "56.0333°N, 4.8167°W")
            ]
        },
        "FRANCE": {
            "ICBM": [],
            "SLBM": [
                ("M51.3", "Le Terrible (S619)", "Ile Longue Naval Base, Brest", "48.3167°N, 4.6000°W"),
                ("M51.2", "Le Triomphant (S616)", "Ile Longue Naval Base, Brest", "48.3167°N, 4.6000°W")
            ]
        },
        "INDIA": {
            "ICBM": ["AGNI-V", "AGNI-VI (TESTING)"],
            "SLBM": [
                ("K-5", "INS Arihant (S2)", "Eastern Naval Command, Visakhapatnam", "17.6868°N, 83.2185°E"),
                ("K-4", "INS Arighaat (S3)", "Eastern Naval Command, Visakhapatnam", "17.6868°N, 83.2185°E")
            ]
        },
        "PAKISTAN": {
            "ICBM": ["SHAHEEN-III"],
            "SLBM": [
                ("BABUR-3 SLCM", "PNS Khalid (Agosta 90B-class)", "Naval Headquarters, Karachi", "24.8607°N, 67.0011°E"),
                ("BABUR-3 SLCM", "PNS Saad (Agosta 90B-class)", "Naval Headquarters, Karachi", "24.8607°N, 67.0011°E")
            ]
        },
        "NORTH KOREA": {
            "ICBM": ["HWASONG-18", "HWASONG-17"],
            "SLBM": [
                ("PUKGUKSong-3", "Sinpo-class SSBN", "Sinpo South Shipyard, South Hamgyong", "40.0333°N, 128.1833°E"),
                ("PUKGUKSong-6 (TESTING)", "Sinpo-class SSBN", "Mayang-do Submarine Base", "39.5333°N, 127.7667°E")
            ]
        },
        "ISRAEL": {
            "ICBM": ["JERICHO III"],
            "SLBM": [
                ("POPEYE TURBO SLCM", "INS Dolphin (Dolphin II-class)", "Haifa Naval Base", "32.7940°N, 34.9896°E"),
                ("POPEYE TURBO SLCM", "INS Tanin (Dolphin II-class)", "Haifa Naval Base", "32.7940°N, 34.9896°E")
            ]
        }
    }
    
    while True:
        print(f"\n{COLOR_GREEN}>>> SELECT MISSILE CATEGORY <<< {COLOR_RESET}")
        print("[1] ICBM (INTERCONTINENTAL BALLISTIC MISSILE)")
        print("[2] SLBM (SUBMARINE LAUNCHED BALLISTIC MISSILE)")
        print(f"\n{COLOR_WHITE}{'COMMAND> '}"); sys.stdout.write(COLOR_RED); sys.stdout.flush()
        cat_cmd = input().strip().upper()
        
        if cat_cmd in ["EXIT", "LOGOUT"]: break
        elif cat_cmd == "LIST GAMES":
            for g in engine.get_game_list(): print(f"  - {g}")
            continue
            
        category = "ICBM" if cat_cmd == "1" or cat_cmd == "ICBM" else "SLBM" if cat_cmd == "2" or cat_cmd == "SLBM" else None
        
        if not category:
            if cat_cmd: print("ILLEGAL CATEGORY.")
            continue
            
        available_weapons = weapons_map[init_nation][category]
        if not available_weapons:
            other_category = "SLBM" if category == "ICBM" else "ICBM"
            other_weapons = weapons_map[init_nation][other_category]
            if other_weapons:
                print(f"{COLOR_YELLOW}NO {category} ASSETS AVAILABLE. SWITCHING TO {other_category}...{COLOR_RESET}")
                time.sleep(1)
                category = other_category
                available_weapons = other_weapons
            else:
                print(f"{COLOR_RED}NO NUCLEAR WEAPONS AVAILABLE FOR {init_nation}{COLOR_RESET}")
                continue
        print(f"\n{COLOR_GREEN}>>> SELECT PAYLOAD DELIVERY SYSTEM ({category}) <<< {COLOR_RESET}")
        if category == "SLBM":
            for i, w in enumerate(available_weapons, 1):
                missile, vessel, location, coords = w
                print(f"\n{COLOR_CYAN}[{i}]{COLOR_RESET} {COLOR_WHITE}{missile}{COLOR_RESET}")
                print(f"    {COLOR_YELLOW}PLATFORM:{COLOR_RESET} {vessel}")
                print(f"    {COLOR_YELLOW}LOCATION:{COLOR_RESET} {location}")
                print(f"    {COLOR_YELLOW}COORDS:{COLOR_RESET}   {coords}")
        else:
            for i, w in enumerate(available_weapons, 1):
                print(f"[{i}] {w}")
            
        print(f"\n{COLOR_WHITE}{'COMMAND> '}"); sys.stdout.write(COLOR_RED); sys.stdout.flush()
        w_cmd = input().strip().upper()
        
        if w_cmd in ["EXIT", "LOGOUT"]: break
        elif w_cmd.isdigit() and 1 <= int(w_cmd) <= len(available_weapons):
            weapon_choice = available_weapons[int(w_cmd)-1]
            run_war_scenario(init_nation, data_mgr, weapon_choice)
        else:
            breach_protocol_initiated()

def start_server_during_boot():
    """Start server during bootup and wait for BOTH ALPHA and BRAVO decoders"""
    global server_socket, clients, current_codes
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 55555))
        server_socket.listen(5)
        
        print(f"{COLOR_CYAN}Initializing decoder connection system...")
        print(f"{COLOR_WHITE}Waiting for BOTH ALPHA and BRAVO decoders to connect...")
        print(f"{COLOR_YELLOW}NOTE: WOLF_OS will NOT start until BOTH decoders are connected!{COLOR_RESET}")
        
        clients = []
        current_codes = ("ALPHA-INIT", "BRAVO-INIT")
        connected_decoders = set()  # Tracks which decoders are connected
        client_info = {}  # Maps socket to decoder type
        
        # Wait for BOTH ALPHA and BRAVO to connect
        while not ("ALPHA" in connected_decoders and "BRAVO" in connected_decoders):
            try:
                print(f"\n{COLOR_WHITE}Status: Waiting for decoder connections...")
                print(f"{COLOR_CYAN}Connected: {list(connected_decoders) if connected_decoders else 'None'}")
                print(f"{COLOR_YELLOW}Required: ALPHA and BRAVO")
                
                # Set timeout so we can update status periodically
                server_socket.settimeout(5.0)
                
                try:
                    client_socket, address = server_socket.accept()
                except socket.timeout:
                    continue
                
                # Reset timeout for normal operation
                server_socket.settimeout(None)
                
                clients.append(client_socket)
                
                # Send initial codes and wait for decoder to identify itself
                message = json.dumps({
                    'type': 'handshake',
                    'message': 'Please identify as ALPHA or BRAVO',
                    'timestamp': time_module.time()
                })
                client_socket.send(message.encode())
                
                # Try to receive decoder identification
                try:
                    client_socket.settimeout(5.0)
                    response = client_socket.recv(1024).decode()
                    client_socket.settimeout(None)
                    
                    data = json.loads(response) if response else {}
                    decoder_type = data.get('decoder_type', 'UNKNOWN').upper()
                    
                    if decoder_type not in ['ALPHA', 'BRAVO']:
                        # Try to infer from client behavior or assign based on what's needed
                        if "ALPHA" not in connected_decoders:
                            decoder_type = "ALPHA"
                        elif "BRAVO" not in connected_decoders:
                            decoder_type = "BRAVO"
                        else:
                            decoder_type = "EXTRA"
                    
                except:
                    # If we can't identify, assign based on what's needed
                    if "ALPHA" not in connected_decoders:
                        decoder_type = "ALPHA"
                    elif "BRAVO" not in connected_decoders:
                        decoder_type = "BRAVO"
                    else:
                        decoder_type = "EXTRA"
                
                # Check if this decoder type is already connected
                if decoder_type in connected_decoders:
                    print(f"{COLOR_RED}✗ {decoder_type} decoder already connected! Rejecting duplicate.")
                    client_socket.close()
                    clients.remove(client_socket)
                    continue
                
                if decoder_type not in ['ALPHA', 'BRAVO']:
                    print(f"{COLOR_RED}✗ Unknown decoder type. Rejecting connection.")
                    client_socket.close()
                    clients.remove(client_socket)
                    continue
                
                # Valid decoder connected
                connected_decoders.add(decoder_type)
                client_info[client_socket] = decoder_type
                
                # Prepare codes
                raw_message = json.dumps({
                    'type': 'codes',
                    'alpha': current_codes[0],
                    'bravo': current_codes[1],
                    'encrypted': True,
                    'timestamp': time_module.time()
                })
                
                # Encrypt with military-grade AES-256-GCM
                encrypted_message = crypto_mgr.encrypt_message(raw_message)
                client_socket.send(encrypted_message.encode())
                
                print(f"{COLOR_GREEN}✓ {decoder_type} decoder connected from {address[0]}:{address[1]}")
                print(f"{COLOR_WHITE}Status: {len(connected_decoders)}/2 decoders connected")
                print(f"{COLOR_CYAN}Connected decoders: {sorted(list(connected_decoders))}")
                
                # Check if both are now connected
                if "ALPHA" in connected_decoders and "BRAVO" in connected_decoders:
                    print(f"\n{COLOR_GREEN}{'='*80}")
                    print(f"{COLOR_GREEN}{'*** BOTH DECODERS CONNECTED ***':^80}")
                    print(f"{COLOR_GREEN}{'='*80}")
                    print(f"{COLOR_GREEN} ALPHA decoder: ONLINE")
                    print(f"{COLOR_GREEN} BRAVO decoder: ONLINE")
                    print(f"{COLOR_CYAN}Proceeding with WOLF_OS boot sequence...")
                    time_module.sleep(2)
                    return True
                
                # Start client handler for this decoder
                def handle_client(client_socket, address, decoder_type):
                    try:
                        while True:
                            try:
                                data = client_socket.recv(1024).decode()
                                if not data:
                                    break
                                if data == 'ACK':
                                    print(f"{COLOR_CYAN}Acknowledgment from {decoder_type} decoder")
                            except:
                                break
                            time_module.sleep(1)
                    except:
                        pass
                    finally:
                        print(f"{COLOR_RED}✗ {decoder_type} decoder disconnected!")
                        if client_socket in clients:
                            clients.remove(client_socket)
                        if decoder_type in connected_decoders:
                            connected_decoders.remove(decoder_type)
                        client_socket.close()
                
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address, decoder_type))
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                print(f"\n{COLOR_RED}Server startup interrupted by user")
                return False
            except Exception as e:
                print(f"{COLOR_RED}Connection error: {e}")
                continue
        
        # Should have returned True above if both connected
        return False
            
    except Exception as e:
        print(f"{COLOR_RED}Server initialization failed: {e}")
        return False
    finally:
        if server_socket:
            server_socket.close()

if __name__ == "__main__":
    try: 
        # Start server during bootup, then proceed to main interface
        if start_server_during_boot():
            # Normal launch sequence after successful decoder connections
            system_boot_sequence()
            display_disclaimer()
            if not login_screen(): 
                sys.exit(0)
            data_mgr = DataManager()
            engine = ScenarioEngine()
            clear_screen()
            main_menu_loop(data_mgr, engine)
        else:
            print(f"{COLOR_RED}Failed to establish decoder connections. System halted.")
            input("Press Enter to exit...")
    except Exception as e: print(f"{COLOR_RED}CRITICAL ERROR: {e}"); input()
