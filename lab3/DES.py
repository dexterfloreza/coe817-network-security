from Crypto.Cipher import DES
import base64

class DESAlgorithm:
    def __init__(self, key):
        if len(key) != 8:
            raise ValueError("Key must be 8 bytes long for DES.")
        self.encrypt_cipher = DES.new(key, DES.MODE_ECB)
        self.decrypt_cipher = DES.new(key, DES.MODE_ECB)

    def pad(self, data):
        # pads the data to ensure that data is a multiple of 8 bytes. 
        return data + b" " * (8 - len(data) % 8)

    def encrypt(self, to_encrypt):
        # encrypts data using DES (ECB) mode
        if isinstance(to_encrypt, str):
            to_encrypt = to_encrypt.encode()  # Convert string to bytes

        padded_data = self.pad(to_encrypt)  # Ensure 8-byte alignment
        encrypted = self.encrypt_cipher.encrypt(padded_data)
        return encrypted

    def decrypt(self, to_decrypt):
        #decrypts DES-encrypted data.
        decrypted = self.decrypt_cipher.decrypt(to_decrypt)
        return decrypted.rstrip(b" ")  # Remove padding spaces


# Example usage
if __name__ == "__main__":
    key = b"8bytekey"  # DES requires an 8-byte key
    des = DESAlgorithm(key)
    
    encrypted_text = des.encrypt("Hello")
    print("Encrypted:", encrypted_text)
    
    decrypted_text = des.decrypt(encrypted_text)
    print("Decrypted:", decrypted_text)
