from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# ==============================
# 🔹 Generate RSA Key Pair
# ==============================
def generate_key_pair():
    """Generates an RSA key pair (public & private)."""
    key = RSA.generate(2048)  # 2048-bit strong key
    public_key = key.publickey()
    return public_key, key  # (Public, Private)

# ==============================
# 🔹 Save RSA Key to File
# ==============================
def save_key(filename, key):
    """Saves an RSA key to a file."""
    with open(filename, "wb") as f:
        f.write(key.export_key())

# ==============================
# 🔹 Load RSA Key from File
# ==============================
def load_key(filename):
    """Loads an RSA key from a file."""
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

# ==============================
# 🔹 Encrypt Data with RSA
# ==============================
def encrypt_rsa(message, public_key):
    """
    Encrypts a message using RSA.
    - Input: message (bytes), public_key (RSA key)
    - Output: encrypted message (bytes)
    """
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message  # Return as raw bytes

# ==============================
# 🔹 Decrypt Data with RSA
# ==============================
def decrypt_rsa(encrypted_message, private_key):
    """
    Decrypts an RSA-encrypted message.
    - Input: encrypted_message (bytes), private_key (RSA key)
    - Output: decrypted message (bytes)
    """
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message  # Return as raw bytes
