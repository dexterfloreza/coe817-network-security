import socket
import os
import pickle
from public_key_auth import public_KeyAuthentication

class alice_client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.public_key_obj = public_KeyAuthentication()
        self.public_key_obj.generate_key_pairs()
        
    def run_alice(self):
        # Generate Alice's nonce
        alice_nonce = os.urandom(17)
        print(f"Alice created nonce: {alice_nonce}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port))
            
            # Sending Alice's public key and nonce info to Bob
            data = pickle.dumps((self.public_key_obj.serialize_publicKey(), alice_nonce))
            client.sendall(data)
            
            # Get encrypted message from Bob
            encrypted_msg = client.recv(4096)
            decrypted_msg = self.public_key_obj.decrypt_privateKey(encrypted_msg)
            received_NA, bob_nonce = decrypted_msg[:16], decrypted_msg[:16]
            
            print(f"Alice received: NA = {received_NA}, NB = {bob_nonce}")
            
            # Verify Alice's nonce
            if received_NA == alice_nonce:
                print("Alice's nonce is verified.")
                
            # Encrypt Bob's nonce and send it back to Bob
            encrypted_response = self.public_key_obj.encrypt_publicKey(
                self.public_key_obj.deserialize_publicKey(self.public_key_obj.serialize_publicKey()), # Bob's key placeholder
                bob_nonce
            )
            client.sendall(encrypted_response)
            
            print("Alice sent encrypted NB to Bob.")
