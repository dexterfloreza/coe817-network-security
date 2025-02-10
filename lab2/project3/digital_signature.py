# digital_signature.py
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import datetime

# Generate RSA key pair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Sign message with Alice's private key
def sign_message(private_key, message):
    key = RSA.import_key(private_key)
    message_bytes = message.encode()
    hashed_message = SHA256.new(message_bytes)
    signature = pkcs1_15.new(key).sign(hashed_message)
    return base64.b64encode(signature).decode()

# Verify signature using Alice's public key
def verify_signature(public_key, message, signature):
    key = RSA.import_key(public_key)
    message_bytes = message.encode()
    hashed_message = SHA256.new(message_bytes)
    try:
        pkcs1_15.new(key).verify(hashed_message, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False

