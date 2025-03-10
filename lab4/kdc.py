import socket
import os
import threading
import datetime
from rsa_utils import load_key, encrypt_rsa, decrypt_rsa
from DES import DESAlgorithm

clients = {}

def start_kdc():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 4888))
    server.listen(3)
    print("🔐 KDC is listening on port 4888...")

    # Accept connections from all three clients
    for _ in range(3):
        conn, addr = server.accept()
        client_id = conn.recv(1024).decode().strip()
        print(f"🔗 Connected to {client_id}: {addr}")
        clients[client_id] = conn

    # Generate a single session key (Ks) for group communication
    Ks = os.urandom(8)

    # Encrypt and send Ks to all three clients
    for client_id, conn in clients.items():
        encrypted_Ks = encrypt_rsa(Ks, load_key(f"{client_id}PublicKey.pem"))
        conn.sendall(encrypted_Ks)
        print(f"🔑 Sent session key Ks to {client_id}")

    print("✅ Key distribution complete. Clients can now chat securely.")

    des = DESAlgorithm(Ks)

    # Communication loop: Handle turns (Alice → Bob → Charlie)
    order = ["Alice", "Bob", "Charlie"]
    while True:
        for sender in order:
            conn = clients[sender]
            try:
                # Receive encrypted message
                encrypted_msg = conn.recv(1024)
                if not encrypted_msg:
                    continue  # Skip if empty

                # Decrypt and timestamp message
                decrypted_msg = des.decrypt(encrypted_msg).decode()
                timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                full_msg = f"{timestamp} {sender}: {decrypted_msg}"

                print(f"📩 {full_msg}")  # Print for KDC logs

                # Encrypt message again and send to other clients
                encrypted_broadcast = des.encrypt(full_msg.encode())
                for receiver, recv_conn in clients.items():
                    if receiver != sender:
                        recv_conn.sendall(encrypted_broadcast)

            except Exception as e:
                print(f"❌ Error forwarding message from {sender}: {e}")
                continue

start_kdc()
