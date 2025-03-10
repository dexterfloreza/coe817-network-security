import socket
import datetime
from rsa_utils import load_key, decrypt_rsa
from DES import DESAlgorithm

def alice():
    print("🚀 Alice starting...")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 4888))

    conn.sendall(b"Alice")

    # Receive and decrypt session key
    encrypted_Ks = conn.recv(1024)
    Ks = decrypt_rsa(encrypted_Ks, load_key("AlicePrivateKey.pem"))
    print(f"🔑 Alice received session key Ks: {Ks}")

    des = DESAlgorithm(Ks)

    # Alice sends a message first
    msg = input("📩 Alice, enter your message: ")
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    encrypted_msg = des.encrypt(msg.encode())

    conn.sendall(encrypted_msg)

    # Receive messages from Bob and Charlie
    while True:
        encrypted_msg = conn.recv(1024)
        decrypted_msg = des.decrypt(encrypted_msg).decode()
        print(f"📩 {decrypted_msg}")

alice()
