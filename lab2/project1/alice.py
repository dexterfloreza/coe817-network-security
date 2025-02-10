# alice.py
import socket
import json
from symmetric_key import encrypt_message, decrypt_message

class Alice:
    def __init__(self):
        self.ID_A = "A"
        self.nonce_A = "1234"
    
    def initiate_communication(self, bob_host, bob_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("[Alice] Connecting to Bob...")
                s.connect((bob_host, bob_port))
                print("[Alice] Connected!")
                
                message_1 = json.dumps({"ID": self.ID_A, "Nonce": self.nonce_A})
                s.sendall(message_1.encode())
                print(f"[Alice] Sent: {message_1}")
                
                response_1 = s.recv(1024).decode()
                response_data = json.loads(response_1)
                nonce_B = response_data["Nonce_B"]
                encrypted_data = response_data["Encrypted"]
                
                decrypted_data = decrypt_message(encrypted_data)
                print(f"[Alice] Decrypted response: {decrypted_data}")
                
                encrypted_final = encrypt_message(json.dumps({"ID": self.ID_A, "Nonce": nonce_B}))
                s.sendall(encrypted_final.encode())
                print(f"[Alice] Sent encrypted final message: {encrypted_final}")
        except Exception as e:
            print(f"[Alice] Error: {e}")

if __name__ == "__main__":
    alice = Alice()
    alice.initiate_communication("127.0.0.1", 65432)
    print("Hello World")
