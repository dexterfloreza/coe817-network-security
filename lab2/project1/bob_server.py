# bob_server.py
import socket
import json
from symmetric_key import encrypt_message, decrypt_message

class Bob:
    def __init__(self):
        self.ID_B = "B"
    
    def start_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("Bob is listening for Alice...")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                request_1 = conn.recv(1024).decode()
                request_data = json.loads(request_1)
                nonce_A = request_data["Nonce"]
                print(f"Bob received: ID_A={request_data['ID']}, Nonce_A={nonce_A}")
                
                nonce_B = "5678"
                encrypted_message = encrypt_message(json.dumps({"ID": self.ID_B, "Nonce": nonce_A}))
                response = json.dumps({"Nonce_B": nonce_B, "Encrypted": encrypted_message})
                conn.sendall(response.encode())
                print(f"Bob sent: Nonce_B={nonce_B}, Encrypted={encrypted_message}")
                
                final_message = conn.recv(1024).decode()
                decrypted_final = decrypt_message(final_message)
                print(f"Bob received decrypted: {decrypted_final}")

if __name__ == "__main__":
    bob = Bob()
    bob.start_server("127.0.0.1", 65432)
