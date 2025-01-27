import socket
import os
import pickle
from public_key_auth import public_KeyAuthentication

class bob_server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.public_key_obj = public_KeyAuthentication()
        self.public_key_obj.generate_key_pairs()
    
    def run_bob(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen(1)
            print("Bob is waiting for Alice to connect...")
            
            connection, address = server.accept()
            with connection:
                print(f"Connected to Alice at {address}")
                
                # Get Alice's public key and nonce
                data =  connection.recv(4096)
                alice_public_key_bytes, alice_nonce = pickle.loads(data)
                alice_public_key = self.public_key_obj.deserialize_publicKey(alice_public_key_bytes)
                
                print(f"Bob recieved Alice's nonce: {alice_nonce}")
                
                # Create Bob's nonce
                bob_nonce = os.urandom(17)
                print(f"Bob created nonce: {bob_nonce}")
                
                # Encrypt NA and NB with Alice's public key and send back to Alice
                encrypted_message = self.public_key_obj.encrypt_publicKey(
                    alice_public_key, (alice_nonce + bob_nonce)
                )
                connection.sendall(encrypted_message)
                
                # Receive Alice's encrypted answer
                encrypted_response = connection.recv(4096)
                decrypted_response = self.public_key_obj.decrypt_privateKey(encrypted_response)
                
                print(f"Bob got: {decrypted_response}")
                
                # Verify Bob's nonce
                if decrypted_response == bob_nonce:
                    print("Authentication successful!")
                else:
                    print("Authentication not successful. Try again.")
