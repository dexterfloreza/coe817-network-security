from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class public_KeyAuthentication:
    def __init__(self):
        self.privateKey = None
        self.publicKey = None
        
    # Method that creates the public and private RSA key pairs
    def generate_key_pairs(self):
        self.privateKey = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048
        )
        
        self.publicKey = self.privateKey.public_key()
        
    
    # Serialize the public key to send to socket
    def serialize_publicKey(self):
        return self.publicKey.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    @staticmethod
    # Deserialize the public key from socket 
    def deserialize_publicKey(public_key_bytes):
        return serialization.load_pem_public_key(public_key_bytes)
    
    # Encryption using RSA public key
    def encrypt_publicKey(self, publicKey, msg):
        return publicKey.encrypt(
            msg,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label = None
            )
        )
        
    def decrypt_privateKey(self, ciphertext):
        return self.privateKey.decrypt(
            ciphertext,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
    
    