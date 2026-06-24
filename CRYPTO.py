import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class MilitaryCryptoManager:
    """Military-grade AES-256-GCM encryption manager"""
    
    def __init__(self, shared_secret="WOLF_CORP_SECURE_2026"):
        self.key = hashlib.sha256(shared_secret.encode()).digest()

    def encrypt_message(self, message):
        """Encrypt message with AES-256-GCM"""
        iv = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        
        ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
        # Combine IV + ciphertext + auth tag
        encrypted_data = iv + ciphertext + encryptor.tag
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt_message(self, encrypted_data):
        """Decrypt message with AES-256-GCM"""
        try:
            data = base64.b64decode(encrypted_data.encode('utf-8'))
            iv = data[:12]
            ciphertext = data[12:-16]
            tag = data[-16:]
            
            decryptor = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv, tag),
                backend=default_backend()
            ).decryptor()
            
            return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
        except Exception as e:
            # For backward compatibility or debugging
            return None
