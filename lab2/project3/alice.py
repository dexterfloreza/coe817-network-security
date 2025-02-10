# alice.py
import socket
import json
import datetime
from digital_signature import generate_rsa_keys, sign_message

class Alice:
    def __init__(self):
        self.private_key, self.public_key = generate_rsa_keys()  # Generate RSA keys
        self.ID_A = "Alice"

    def initiate_communication(self, bob_host, bob_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("[Alice] Connecting to Bob...")
                s.connect((bob_host, bob_port))
                print("[Alice] Connected!")

                message = "Hello, Bob. This is Alice."
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Human-readable timestamp
                data_to_sign = message + timestamp  # Concatenate message with timestamp
                
                signature = sign_message(self.private_key, data_to_sign)

                signed_message = json.dumps({
                    "ID": self.ID_A,
                    "Message": message,
                    "Timestamp": timestamp,
                    "Signature": signature,
                    "PublicKey": self.public_key.decode()  # Send public key for verification
                })

                s.sendall(signed_message.encode())
                print(f"[Alice] Sent signed message: {signed_message}")

        except Exception as e:
            print(f"[Alice] Error: {e}")

if __name__ == "__main__":
    alice = Alice()
    alice.initiate_communication("127.0.0.1", 65432)

