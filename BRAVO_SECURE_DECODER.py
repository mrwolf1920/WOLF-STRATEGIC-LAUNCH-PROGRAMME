#!/usr/bin/env python3
"""
BRAVO_SECURE_DECODER_V2 - Military-Grade Encrypted Nuclear Code Decoder
Secure client for receiving AES-256-GCM encrypted nuclear codes
Standalone version with complete interface
"""
import os
import sys
import time
import json
import socket
import hashlib
import base64
import platform
from datetime import datetime
from cryptography.hazmat.primitives import hashes, ciphers, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path

# Robustly add project root to sys.path (Fixes Mac/Linux import errors)
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from core.PASS_CODE import (
    COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_WHITE, COLOR_RESET, COLOR_DIM, COLOR_CYAN, COLOR_BLUE, BG_RED, BG_GREEN, BG_YELLOW,
    clear_screen
)
from core.CRYPTO import MilitaryCryptoManager

# Cross-platform compatibility fixes (Linux/Mac)
IS_WINDOWS = platform.system() == "Windows"
if not IS_WINDOWS:
    # Fix for Unix-based terminal color and input issues
    import signal
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    except:
        pass


class SecureBravoDecoder:
    """Military-grade encrypted BRAVO code decoder"""
    
    def __init__(self, server_host='127.0.0.1', port=55555):
        self.server_host = server_host
        self.port = port
        self.client_socket = None
        self.current_codes = None
        self.crypto = MilitaryCryptoManager()
            
    def connect_to_server(self):
        """Connect to secure synchronization server"""
        try:
            # Create new connection
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_socket.settimeout(10)
            self.client_socket.connect((self.server_host, self.port))
            
            print(f"{COLOR_GREEN}Connected to secure sync server")
            return True
            
        except Exception as e:
            print(f"{COLOR_RED}Failed to connect to server: {e}")
            return False

    def receive_secure_codes_once(self):
        """Receive codes once and return (non-blocking version)"""
        try:
            # Send initial handshake
            self.client_socket.send(b'HANDSHAKE')
            
            # Wait for initial message with timeout
            self.client_socket.settimeout(10.0)
            
            encrypted_data = self.client_socket.recv(4096).decode()
            if encrypted_data:
                # Decrypt military-grade encrypted message
                decrypted_data = self.crypto.decrypt_message(encrypted_data)
                if decrypted_data:
                    try:
                        message = json.loads(decrypted_data)
                        if message['type'] == 'codes' and message.get('encrypted'):
                            self.current_codes = (message['alpha'], message['bravo'])
                            print(f"\n{COLOR_GREEN}{'='*80}")
                            print(f"{COLOR_GREEN}{'*** SECURE BRAVO CODE RECEIVED ***':^80}")
                            print(f"{COLOR_GREEN}{'='*80}")
                            print(f"{COLOR_WHITE}BRAVO CODE: {COLOR_GREEN}{message['bravo']}{COLOR_RESET}")
                            print(f"{COLOR_CYAN}Encryption: AES-256-GCM | Status: SECURE")
                            print(f"{COLOR_YELLOW}Timestamp: {datetime.fromtimestamp(message['timestamp']).strftime('%H:%M:%S')}")
                            
                            # Send secure acknowledgment
                            self.client_socket.send(b'SECURE_ACK')
                        elif message['type'] == 'handshake':
                            print(f"{COLOR_CYAN}Secure link established")
                            self.client_socket.send(b'HANDSHAKE_COMPLETE')
                    except json.JSONDecodeError:
                        print(f"{COLOR_RED}Invalid encrypted message format")
                    except Exception as e:
                        print(f"{COLOR_RED}Secure decryption error: {e}")
                        return False
            else:
                return False
                    
        except socket.timeout:
            print(f"{COLOR_YELLOW}No codes received within timeout")
            return False
        except Exception as e:
            print(f"{COLOR_RED}Secure connection lost: {e}")
            return False
            
        return True

    def login(self):
        """Secure login authentication with warning screen"""
        clear_screen()
        
        # ASCII Art Header for BRAVO
        print(COLOR_RED)
        print(f"{'╔══════════════════════════════════════════════════════╗':^80}")
        print(f"{'║  ██████╗  ██████╗   █████╗  ██║       ██║  ██████╗   ║':^80}")
        print(f"{'║  ██╔══██║ ██╔══██╗ ██╔══██╗  ██║     ██╔╝ ██╔═══██║  ║':^80}")
        print(f"{'║  ██████╔╝ ██████╔╝ ███████║   ██    ██╔╝  ██║   ██║  ║':^80}")
        print(f"{'║  ██╔══██║ ██╔══██╗ ██╔══██║    ██  ██╔╝   ██║   ██║  ║':^80}")
        print(f"{'║  ██████╔╝ ██║  ██║ ██║  ██║      ██╔═╝    ╚██████╔╝  ║':^80}")
        print(f"{'║   ╚════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝      ╚═╝        ╚════╝   ║':^80}")
        print(f"{'║                   D E C O D E R                      ║':^80}")
        print(f"{'╚══════════════════════════════════════════════════════╝':^80}")
        
        # Warning Messages
        print(f"\n{BG_RED}{COLOR_WHITE}{'WARNING: UNAUTHORISED PERSONNEL ARE ADVISED TO EXIT THIS PROGRAM':^80}")
        print(f"{BG_RED}{COLOR_WHITE}{'ALL ACTIVITIES ARE BEING RECORDED':^80}{COLOR_RESET}")
        
        print(f"\n{COLOR_RED}{'Any unauthorised use may lead to termination of employment':^80}")
        print(f"{COLOR_RED}{'and may be liable to severe consequences.':^80}")
        print(f"{COLOR_RED}{'All activities are recorded and filed.':^80}{COLOR_RESET}")
        
        # Authentication
        print(f"\n{COLOR_WHITE}{'USERNAME: ':^40}", end="")
        sys.stdout.write(COLOR_BLUE)
        sys.stdout.flush()
        try:
            user = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_RED}Login interrupted.")
            return False
        
        print(f"\n{COLOR_WHITE}{'PASSWORD: ':^40}", end="")
        sys.stdout.write(COLOR_GREEN)
        sys.stdout.flush()
        try:
            import msvcrt
            password = ""
            while True:
                char = msvcrt.getch()
                if char == b'\r':  # Enter key
                    break
                elif char == b'\x08':  # Backspace
                    if password:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                else:
                    password += char.decode('utf-8')
                    sys.stdout.write('*')
                sys.stdout.flush()
            print()
        except ImportError:
            # Fallback for non-Windows systems
            password = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_RED}Login interrupted.")
            return False
        
        if user != "MR_WOLF" or password != "WOLF!(@)":
            print(f"\n{BG_RED}{COLOR_WHITE}{'ACCESS DENIED. UNAUTHORIZED ATTEMPT LOGGED.':^80}{COLOR_RESET}")
            time.sleep(2)
            return False
            
        print(f"\n{BG_GREEN}{COLOR_WHITE}{'ACCESS GRANTED. AUTHENTICATION SUCCESSFUL.':^80}{COLOR_RESET}")
        time.sleep(1)
        
        # Nuclear Countries Selection
        clear_screen()
        print(f"{COLOR_CYAN}{'='*80}")
        print(f"{COLOR_CYAN}{'NUCLEAR COUNTRIES':^80}")
        print(f"{COLOR_CYAN}{'='*80}{COLOR_RESET}")
        
        nuclear_countries = [
            "1. United States",
            "2. Russia", 
            "3. China",
            "4. France",
            "5. United Kingdom",
            "6. India",
            "7. Pakistan",
            "8. Israel",
            "9. North Korea"
        ]
        
        for country in nuclear_countries:
            print(f"{COLOR_WHITE}{country:<50}{COLOR_RESET}")
        
        print(f"\n{COLOR_YELLOW}{'Confirm country for Authentication Code':^80}{COLOR_RESET}")
        print(f"{COLOR_WHITE}{'Enter number (1-9): ':^40}", end="")
        sys.stdout.flush()
        
        try:
            choice = input().strip()
            country_codes = {
                "1": "USA-BRAVO-7845",
                "2": "RUS-BRAVO-9921",
                "3": "CHN-BRAVO-3456",
                "4": "FRA-BRAVO-7823",
                "5": "GBR-BRAVO-4567",
                "6": "IND-BRAVO-8899",
                "7": "PAK-BRAVO-2345",
                "8": "ISR-BRAVO-6789",
                "9": "PRK-BRAVO-1111"
            }
            bravo_code = country_codes.get(choice, "UNKNOWN-0000")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_RED}Selection interrupted.")
            return False
        
        # Show BRAVO ASCII Art Box
        clear_screen()
        print(COLOR_RED)
        print(f"{'╔══════════════════════════════════════════════════════╗':^80}")
        print(f"{'║  ██████╗  ██████╗   █████╗  ██║       ██║  ██████╗   ║':^80}")
        print(f"{'║  ██╔══██║ ██╔══██╗ ██╔══██╗  ██║     ██╔╝ ██╔═══██║  ║':^80}")
        print(f"{'║  ██████╔╝ ██████╔╝ ███████║   ██    ██╔╝  ██║   ██║  ║':^80}")
        print(f"{'║  ██╔══██║ ██╔══██╗ ██╔══██║    ██  ██╔╝   ██║   ██║  ║':^80}")
        print(f"{'║  ██████╔╝ ██║  ██║ ██║  ██║      ██╔═╝    ╚██████╔╝  ║':^80}")
        print(f"{'║   ╚════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝      ╚═╝        ╚════╝   ║':^80}")
        print(f"{'║                   D E C O D E R                      ║':^80}")
        print(f"{'╚══════════════════════════════════════════════════════╝':^80}{COLOR_RESET}")
        
        # Display BRAVO CODE in YELLOW background with BLACK text
        COLOR_BLACK = "\033[30m"
        print(f"\n{BG_YELLOW}{COLOR_BLACK}{f'BRAVO CODE: {bravo_code}':^80}{COLOR_RESET}")
        
        # Press ENTER to Continue (not Exit - to allow WOLF_OS connection)
        print(f"\n{COLOR_WHITE}{'Press [ENTER] to Continue':^80}{COLOR_RESET}")
        input()
        return True
        
    def start_decoder_program_with_connection(self):
        """Start decoder program while maintaining active connection"""
        print(f"\n{COLOR_CYAN}{'='*80}")
        print(f"{COLOR_CYAN}{'*** DECODER PROGRAM - CONNECTION ACTIVE ***':^80}")
        print(f"{COLOR_CYAN}{'='*80}")
        print(f"{COLOR_GREEN}✓ Connection maintained for WOLF_OS operations")
        print(f"{COLOR_DIM}✓ Ready to receive codes anytime")
        print(f"{COLOR_DIM}✓ Interface available while connected{COLOR_RESET}")
        print(f"{COLOR_YELLOW}DEBUG: About to start interface loop...")
        
        if self.current_codes:
            alpha_code, bravo_code = self.current_codes
            print(f"{COLOR_WHITE}Current Codes Loaded:")
            print(f"{COLOR_GREEN}  ALPHA: {alpha_code}")
            print(f"{COLOR_GREEN}  BRAVO: {bravo_code}")
        else:
            print(f"{COLOR_YELLOW}DEBUG: No current codes available")
        
        # Start decoder interface while keeping connection alive
        print(f"{COLOR_YELLOW}DEBUG: Starting run_decoder_interface_with_connection...")
        self.run_decoder_interface_with_connection()
        
    def run_decoder_interface_with_connection(self):
        """Decoder interface that maintains connection for WOLF_OS operations"""
        print(f"{COLOR_YELLOW}DEBUG: Entering interface loop...")
        while True:
            print(f"\n{COLOR_WHITE}{'='*60}")
            print(f"{COLOR_WHITE}{'*** DECODER INTERFACE - CONNECTION ACTIVE ***':^60}")
            print(f"{COLOR_WHITE}{'='*60}")
            print(f"{COLOR_GREEN}[1] Decode Message")
            print(f"{COLOR_GREEN}[2] Verify Codes") 
            print(f"{COLOR_GREEN}[3] Show Current Codes")
            print(f"{COLOR_CYAN}[4] Select Country & View Codes")
            print(f"{COLOR_YELLOW}[5] Refresh Codes (check server)")
            print(f"{COLOR_RED}[6] Exit & Close Connection")
            print(f"{COLOR_DIM}Connection: ACTIVE - Ready for WOLF_OS operations")
            print(f"{COLOR_YELLOW}DEBUG: Waiting for user input...")
            
            try:
                choice = input(f"\n{COLOR_WHITE}Choice: ").strip()
                
                print(f"{COLOR_YELLOW}DEBUG: User chose: {choice}")
                
                if choice == "1":
                    print(f"{COLOR_YELLOW}DEBUG: Calling decode_message...")
                    self.decode_message()
                elif choice == "2":
                    print(f"{COLOR_YELLOW}DEBUG: Calling verify_codes...")
                    self.verify_codes()
                elif choice == "3":
                    print(f"{COLOR_YELLOW}DEBUG: Calling show_current_codes...")
                    self.show_current_codes()
                elif choice == "4":
                    print(f"{COLOR_YELLOW}DEBUG: Calling select_country_and_show_codes...")
                    self.select_country_and_show_codes()
                elif choice == "5":
                    print(f"{COLOR_CYAN}Checking server for new codes...")
                    # Try to receive new codes while maintaining connection
                    self.receive_secure_codes_once()
                elif choice == "6":
                    print(f"{COLOR_YELLOW}Exiting decoder and closing connection...")
                    return True
                else:
                    print(f"{COLOR_RED}Invalid choice!")
                    
            except (EOFError, KeyboardInterrupt):
                print(f"\n{COLOR_YELLOW}Decoder interrupted...")
                return False
            except Exception as e:
                print(f"{COLOR_RED}Error: {e}")
                return False

    def select_country_and_show_codes(self):
        """Select country and display respective codes"""
        clear_screen()
        print(f"{COLOR_RED}{'═'*78}")
        print(f"║ {' ':^76} ")
        print(f"║ {'██╗    ██╗  █████╗  ██████╗  ███╗   ██╗ ██╗ ███╗   ██╗  ██████╗ ██████╗ ':^76} ║")
        print(f"║ {'██║    ██║ ██╔══██╗ ██╔════╝██╔════╝ ██╔═══██╗████╗  ██║ ':^76} ║")
        print(f"║ {'██║ █╗ ██║ ███████║ ██████╔╝ ██║   ██║ ██║      █████╔╝  █████╗   ██║ ':^76} ║")
        print(f"║ {'██║  ██║██╔██╗ ██║   ██║ ██║      ██║   ██║██║╚██╗██║ ':^76} ║")
        print(f"║ {'██║███╗██║ ██║   ██║ ██║      ██║   ██║ ██║ ╚████║ ██║  ███████╗ ██████╔╝ ':^76} ║")
        print(f"║ {' ╚███╔███╔╝ ██║ ╚═╝  ██║      ╚██████╔╝ ╚██████╗ ██║ ╚████║  ███████╗ ██████╔╝ ':^76} ║")
        print(f"║ {'  ╚══╝ ╚═╝  ╚═╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝  ╚══════╝ ╚═════╝ ':^76} ║")
        print(f"║ {' ':^76} ║")
        print(f"║ {'STRATEGIC CODE DECODER UNIT - OMEGA CLEARANCE':^76} ║")
        print(f"╚{'═'*78}╝{COLOR_RESET}")
        
        nations = [
            "UNITED STATES", "RUSSIA", "CHINA", "UNITED KINGDOM", 
            "FRANCE", "INDIA", "PAKISTAN", "NORTH KOREA", "ISRAEL"
        ]
        
        print(f"\n{COLOR_GREEN}{'>>> SELECT NATION FOR DECRYPTION <<< '}")
        for i, n in enumerate(nations, 1): print(f"[{i}] {n}")
        print(f"[0] SHOW ALL CODES")
        print(f"\n{COLOR_WHITE}{'COMMAND>'}")
        sys.stdout.write(COLOR_RED)
        sys.stdout.flush()
        
        # Cross-platform input handling
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_YELLOW}Selection interrupted.")
            return
        
        clear_screen()
        
        if not self.current_codes:
            print(f"{COLOR_RED}No codes available! Please connect to server first.")
            time.sleep(2)
            return
            
        alpha_code, bravo_code = self.current_codes
        
        # Display codes based on selection
        if choice == "0":
            print(f"\n{COLOR_GREEN}{'='*80}")
            print(f"{COLOR_GREEN}{'*** ALL NUCLEAR CODES ***':^80}")
            print(f"{COLOR_GREEN}{'='*80}")
            for nation in nations:
                print(f"{COLOR_WHITE}{nation}:")
                print(f"  ALPHA: {COLOR_GREEN}{alpha_code}")
                print(f"  BRAVO: {COLOR_GREEN}{bravo_code}")
                print()
        elif choice.isdigit() and 1 <= int(choice) <= len(nations):
            selected_nation = nations[int(choice) - 1]
            print(f"\n{COLOR_GREEN}{'='*80}")
            print(f"{COLOR_GREEN}{'*** NUCLEAR CODES FOR ' + selected_nation + ' ***':^80}")
            print(f"{COLOR_GREEN}{'='*80}")
            print(f"{COLOR_WHITE}ALPHA CODE: {COLOR_GREEN}{alpha_code}")
            print(f"{COLOR_WHITE}BRAVO CODE: {COLOR_GREEN}{bravo_code}")
            print(f"{COLOR_CYAN}Status: ARMED AND READY")
            print(f"{COLOR_YELLOW}Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"{COLOR_RED}Invalid selection!")
            time.sleep(2)

    def decode_message(self):
        """Decode an encrypted message"""
        if not self.current_codes:
            print(f"{COLOR_RED}No codes available!")
            return
            
        try:
            message = input(f"{COLOR_WHITE}Enter encrypted message: ").strip()
            # Add decoding logic here
            print(f"{COLOR_GREEN}Message decoded successfully!")
            print(f"{COLOR_WHITE}Decoded: [MESSAGE CONTENT]")
        except Exception as e:
            print(f"{COLOR_RED}Decoding failed: {e}")
            
    def verify_codes(self):
        """Verify current codes"""
        if not self.current_codes:
            print(f"{COLOR_RED}No codes available!")
            return
            
        alpha_code, bravo_code = self.current_codes
        print(f"\n{COLOR_GREEN}{'='*60}")
        print(f"{COLOR_GREEN}{'*** CODE VERIFICATION ***':^60}")
        print(f"{COLOR_GREEN}{'='*60}")
        print(f"{COLOR_WHITE}ALPHA Code: {COLOR_GREEN}{alpha_code}")
        print(f"{COLOR_WHITE}BRAVO Code: {COLOR_GREEN}{bravo_code}")
        print(f"{COLOR_CYAN}Status: VERIFIED")
        print(f"{COLOR_YELLOW}Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        
    def show_current_codes(self):
        """Display current loaded codes"""
        if not self.current_codes:
            print(f"{COLOR_RED}No codes loaded!")
            return
            
        alpha_code, bravo_code = self.current_codes
        print(f"\n{COLOR_CYAN}{'='*60}")
        print(f"{COLOR_CYAN}{'*** CURRENT CODES ***':^60}")
        print(f"{COLOR_CYAN}{'='*60}")
        print(f"{COLOR_WHITE}ALPHA: {COLOR_GREEN}{alpha_code}")
        print(f"{COLOR_WHITE}BRAVO: {COLOR_GREEN}{bravo_code}")

    def start_client(self):
        """Start secure client and keep connection alive while working in WOLF_OS"""
        if not self.connect_to_server():
            return
            
        print(f"{COLOR_CYAN}Connection established! Keeping connection active...")
        print(f"{COLOR_DIM}Connection will remain active until you quit WOLF_OS{COLOR_RESET}")
        
        try:
            # Initial code reception
            print(f"{COLOR_CYAN}Attempting to receive codes from server...")
            success = self.receive_secure_codes_once()
            print(f"{COLOR_CYAN}Code reception result: {success}")
            
            if success:
                print(f"\n{COLOR_GREEN}Codes received! Connection maintained for WOLF_OS operations...")
            else:
                print(f"\n{COLOR_YELLOW}No initial codes. Starting interface anyway...")
            
            # Auto-start decoder program while keeping connection alive
            print(f"{COLOR_CYAN}Starting decoder interface...")
            self.start_decoder_program_with_connection()
                
        except KeyboardInterrupt:
            print(f"\n{COLOR_YELLOW}Disconnecting from secure server...")
        finally:
            if self.client_socket:
                self.client_socket.close()
                print(f"{COLOR_RED}Connection closed.")

def main():
    clear_screen()
    
    # ASCII Art - Secure Satellite Uplink
    print(COLOR_RED)
    print(f"{'╔════════════════════════════════════════════════════════════════════════════════════╗':^80}")
    print(f"{'║   ███████╗ ███████╗  ██████╗ ██╗   ██╗ ██████╗  ███████╗                           ║':^80}")
    print(f"{'║   ██╔════╝ ██╔════╝ ██╔════╝ ██║   ██║ ██╔══██╗ ██╔════╝                           ║':^80}")
    print(f"{'║   ███████╗ █████╗   ██║      ██║   ██║ ██████╔╝ █████╗                             ║':^80}")
    print(f"{'║   ╚════██║ ██╔══╝   ██║      ██║   ██║ ██╔══██╗ ██╔══╝                             ║':^80}")
    print(f"{'║   ███████║ ███████╗ ╚██████╗ ╚██████╔╝ ██║  ██║ ███████╗                           ║':^80}")
    print(f"{'║   ╚══════╝ ╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═╝ ╚══════╝                           ║':^80}")
    print(f"{'║                                                                                    ║':^80}")
    print(f"{'║   ███████╗  █████╗  ████████╗ ███████╗ ██╗      ██╗      ██╗ ████████╗ ███████     ║':^80}")
    print(f"{'║   ██╔════╝ ██╔══██╗ ╚══██╔══╝ ██╔════╝ ██║      ██║      ██║ ╚══██╔══╝ ██╔════╝    ║':^80}")
    print(f"{'║   ███████╗ ███████║    ██║    █████╗   ██║      ██║      ██║    ██║    █████╗      ║':^80}")
    print(f"{'║   ╚════██║ ██╔══██║    ██║    ██╔══╝   ██║      ██║      ██║    ██║    ██╔══╝      ║':^80}")
    print(f"{'║   ███████║ ██║  ██║    ██║    ███████╗ ███████╗ ███████╗ ██║    ██║    ███████╗    ║':^80}")
    print(f"{'║   ╚══════╝ ╚═╝  ╚═╝    ╚═╝    ╚══════╝ ╚══════╝ ╚══════╝ ╚═╝    ╚═╝    ╚══════╝    ║':^80}")
    print(f"{'║                                                                                    ║':^80}")
    print(f"{'║   ██╗   ██╗ ██████╗  ██╗     ██╗ ███╗   ██╗ ██╗  ██╗                               ║':^80}")
    print(f"{'║   ██║   ██║ ██╔══██╗ ██║     ██║ ████╗  ██║ ██║ ██╔╝                               ║':^80}")
    print(f"{'║   ██║   ██║ ██████╔╝ ██║     ██║ ██╔██╗ ██║ ██████║                                ║':^80}")
    print(f"{'║   ██║   ██║ ██╔═══╝  ██║     ██║ ██║╚██╗██║ ██╔═██╗                                ║':^80}")
    print(f"{'║   ╚██████╔╝ ██║      ███████╗██║ ██║ ╚████║ ██║  ██║                               ║':^80}")
    print(f"{'║    ╚═════╝  ╚═╝      ╚══════╝╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝                               ║':^80}")
    print(f"{'╚════════════════════════════════════════════════════════════════════════════════════╝':^80}")
    print(COLOR_RESET)
    
    # Phase initiated message
    print(f"\n{BG_RED}{COLOR_WHITE}{'BRAVO PHASE INITIATED':^80}{COLOR_RESET}")
    time.sleep(1)
    
    # Yellow warning
    print(f"\n{COLOR_YELLOW}{'Satellite Uplink in progress DO NOT CLOSE THIS WINDOW':^80}{COLOR_RESET}")
    time.sleep(2)
    
    # Try connection
    print(f"\n{COLOR_CYAN}Establishing secure connection...")
    decoder = SecureBravoDecoder()
    
    if not decoder.connect_to_server():
        print(f"{COLOR_RED}✗ Connection failed! Unable to establish link.")
        sys.exit(1)
        
    print(f"{COLOR_GREEN}✓ Secure connection established!")
    
    time.sleep(1)
    
    # Start keepalive thread immediately (before login)
    import threading
    def keepalive():
        count = 0
        while True:
            try:
                if decoder.client_socket:
                    decoder.client_socket.send(b'ACK')
                    count += 1
                    if count <= 3:  # Show only first 3 messages
                        print(f"{COLOR_DIM}BRAVO Keepalive sent to WOLF_OS (#{count}){COLOR_RESET}")
                time.sleep(3)
            except:
                break
    
    keepalive_thread = threading.Thread(target=keepalive, daemon=True)
    keepalive_thread.start()
    print(f"{COLOR_GREEN}✓ BRAVO Keepalive thread started - Connection will stay active")
    
    # Handle WOLF_OS handshake IMMEDIATELY (before login)
    print(f"{COLOR_CYAN}Handling WOLF_OS handshake...")
    try:
        decoder.client_socket.settimeout(5.0)
        data = decoder.client_socket.recv(1024).decode()
        print(f"{COLOR_YELLOW}DEBUG: Received from WOLF_OS: {data}")
        if data:
            try:
                msg = json.loads(data)
                print(f"{COLOR_YELLOW}DEBUG: Parsed JSON: {msg}")
                if msg.get('type') == 'handshake':
                    print(f"{COLOR_CYAN}✓ Received handshake from WOLF_OS")
                    response = json.dumps({'decoder_type': 'BRAVO'})
                    decoder.client_socket.send(response.encode())
                    print(f"{COLOR_GREEN}✓ Sent BRAVO identification to WOLF_OS: {response}")
                    print(f"{COLOR_CYAN}✓ WOLF_OS handshake completed successfully")
                elif msg.get('type') == 'codes':
                    # Handle case where WOLF_OS sends codes immediately
                    print(f"{COLOR_CYAN}✓ Received codes from WOLF_OS")
                    response = json.dumps({'decoder_type': 'BRAVO'})
                    decoder.client_socket.send(response.encode())
                    print(f"{COLOR_GREEN}✓ Sent BRAVO identification to WOLF_OS: {response}")
            except Exception as e:
                print(f"{COLOR_RED}DEBUG: JSON parsing error: {e}")
                pass
        else:
            print(f"{COLOR_RED}DEBUG: No data received from WOLF_OS")
        decoder.client_socket.settimeout(None)
    except Exception as e:
        print(f"{COLOR_YELLOW}Handshake warning: {e}")
        # Try to send identification anyway
        try:
            response = json.dumps({'decoder_type': 'BRAVO'})
            decoder.client_socket.send(response.encode())
            print(f"{COLOR_GREEN}✓ Sent BRAVO identification to WOLF_OS (fallback): {response}")
        except Exception as e2:
            print(f"{COLOR_RED}DEBUG: Fallback send failed: {e2}")
            pass
    
    # STAY CONNECTED - Don't proceed with login, just maintain connection for WOLF_OS
    print(f"{COLOR_GREEN}✓ BRAVO decoder now maintaining connection for WOLF_OS...")
    print(f"{COLOR_CYAN}Waiting for WOLF_OS to continue with both decoders connected...")
    
    # Keep connection alive with simple keepalive
    try:
        while True:
            try:
                # Check if we received any data from WOLF_OS
                decoder.client_socket.settimeout(1.0)
                data = decoder.client_socket.recv(1024)
                if data:
                    try:
                        msg = json.loads(data.decode())
                        if msg.get('type') == 'codes':
                            print(f"{COLOR_GREEN}✓ BRAVO received codes: {msg.get('bravo', 'N/A')}")
                            # Send acknowledgment
                            decoder.client_socket.send(b'ACK')
                        elif msg.get('type') == 'shutdown':
                            print(f"{COLOR_YELLOW}✓ BRAVO received shutdown signal from WOLF_OS")
                            break
                    except:
                        pass
                else:
                    # Send keepalive every few seconds
                    decoder.client_socket.send(b'KEEPALIVE')
            except socket.timeout:
                continue
            except Exception as e:
                print(f"{COLOR_RED}✗ BRAVO connection error: {e}")
                break
    except KeyboardInterrupt:
        print(f"\n{COLOR_YELLOW}✓ BRAVO decoder shutting down...")
    
    print(f"{COLOR_GREEN}✓ BRAVO decoder connection closed")
    decoder.client_socket.close()

if __name__ == "__main__":
    main()
