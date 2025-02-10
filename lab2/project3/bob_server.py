# bob_server.py
import socket
import json
import datetime
from digital_signature import generate_rsa_keys, sign_message
from digital_signature import verify_signature

class Bob:
    def __init__(self):
        self.ID_B = "Bob"

    def start_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("[Bob] Waiting for Alice...")

            conn, addr = s.accept()
            with conn:
                print(f"[Bob] Connected by {addr}")

                received_data = conn.recv(4096).decode()
                received_json = json.loads(received_data)

                alice_id = received_json["ID"]
                message = received_json["Message"]
                timestamp = received_json["Timestamp"]
                signature = received_json["Signature"]
                public_key = received_json["PublicKey"]

                print(f"[Bob] Received message from {alice_id}: {message}")
                print(f"[Bob] Received timestamp: {timestamp}")
                print(f"[Bob] Received signature: {signature}")

                # Verify the signature
                data_to_verify = message + timestamp
                is_valid = verify_signature(public_key, data_to_verify, signature)

                # Convert timestamp to datetime object
                message_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.datetime.now()
                is_fresh = (current_time - message_time).total_seconds() < 30  # Check if within 30 seconds

                if is_valid and is_fresh:
                    print("[Bob] Signature is valid and message is fresh. Authentication successful!")
                elif not is_valid:
                    print("[Bob] Signature verification failed! Possible tampering.")
                else:
                    print("[Bob] Message is too old! Possible replay attack.")

if __name__ == "__main__":
    bob = Bob()
    bob.start_server("127.0.0.1", 65432)