# symmetric_key.py
from Crypto.Cipher import DES
import base64

# DES requires an 8-byte key
KEY = b'8bytekey'

# Function to pad data to be a multiple of 8 bytes

def pad(data):
    while len(data) % 8 != 0:
        data += " "  # Pad with spaces
    return data

# Function to encrypt messages using DES
def encrypt_message(message):
    cipher = DES.new(KEY, DES.MODE_ECB)
    padded_message = pad(message)
    encrypted_bytes = cipher.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_bytes).decode()

# Function to decrypt messages using DES
def decrypt_message(encrypted_message):
    cipher = DES.new(KEY, DES.MODE_ECB)
    try:
        encrypted_bytes = base64.b64decode(encrypted_message)
        decrypted_padded = cipher.decrypt(encrypted_bytes).decode().strip()
        return decrypted_padded
    except Exception as e:
        print(f"[Error] Decryption failed: {e}")
        return None
