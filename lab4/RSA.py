# RSA 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class RSAEncryption:
    def __init__(self):
        self.encrypt_cipher = None
        self.decrypt_cipher = None
    
    def generate_key_pair(self, key_size = 2048):
        # Generate an RSA key pair
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return public_key, private_key
    
    def public_encrypt(self, message, public_key_pem):
        # Encrypt message using a public key
        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted = cipher.encrypt(message.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def private_encrypt(self, message, private_key_pem):
        # Encrypt message using a private key
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        encrypted = cipher.encrypt(message.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def public_decrypt(self, encrypted_message, public_key_pem):
        # Decrypt message using a public key
        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
        return decrypted.decode('utf-8')
    
    def private_decrypt(self, encrypted_message, private_key_pem):
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
        return decrypted.decode('utf-8')
    
# test the implementation
if __name__ == "__main__":
    rsa = RSAEncryption()

    # generate key pair
    public_key, private_key = rsa.generate_key_pair()

    print("Public Key:", public_key.decode())
    print("Private Key:", private_key. decode())

    # Encrypt with public key
    message = "hello world!"
    encrypted = rsa.public_encrypt(message, public_key)
    print("\nEncrypted:", encrypted)

    # Decrypt with private key
    decrypted = rsa.private_decrypt(encrypted, private_key)
    print("Decrypted:", decrypted)
