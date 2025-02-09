import socket
import os
import pickle
from public_key_auth import public_KeyAuthentication

class alice_client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.public_key_obj = public_KeyAuthentication()
        self.public_key_obj.generate_key_pairs()
        
    def run_alice(self):
        try:
            # Generate Alice's nonce
            alice_nonce = os.urandom(16)
            print(f"Alice created nonce: {alice_nonce}")
        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.host, self.port))
            
                # Sending Alice's public key and nonce info to Bob
                data = pickle.dumps((self.public_key_obj.serialize_publicKey(), alice_nonce))
                client.sendall(data)
                # print("Alice sent her public key and nonce to Bob. ")
                
                # Receive Bob's public key from Bob
                bob_public_key_bytes = client.recv(4096)
                bob_public_key = self.public_key_obj.deserialize_publicKey(bob_public_key_bytes)
                # print("Alice recieved Bob's public key. ")
                
                # Get encrypted message from Bob
                encrypted_msg = client.recv(4096)
                print("the recieved message 2")
                decrypted_msg = self.public_key_obj.decrypt_privateKey(encrypted_msg)
                print("the decrypted message 2")
                received_NA, bob_nonce = decrypted_msg[:16], decrypted_msg[16:]
                # print(f"Alice received: NA = {received_NA}, NB = {bob_nonce}")

                # Verify Alice's nonce
                if received_NA == alice_nonce:
                    print("the received message 3")
                else:
                    print("Nonce verification failed.")
                    return # Exit if verification fails
                
                # Encrypt Bob's nonce with Bob's public key
                encrypted_response = self.public_key_obj.encrypt_publicKey(
                    bob_public_key, # Bob's key placeholder
                    bob_nonce
                )
                client.sendall(encrypted_response)
                print("Alice sent encrypted NB to Bob.")
        
        except (ConnectionRefusedError, socket.error) as e:
            print(f"Connection Error: {e}")
        
        except pickle.PickleError as e:
            print(f"Pickle Serialization Error: {e}")
        
        except ValueError as e:
            print(f"Decryption or data handling error: {e}")
        
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")

if __name__ == "__main__":
    alice = alice_client()
    alice.run_alice()

