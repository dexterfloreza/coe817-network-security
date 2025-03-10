import socket
import datetime
from rsa_utils import load_key, decrypt_rsa
from DES import DESAlgorithm

def charlie():
    print("🚀 Charlie starting...")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 4888))

    conn.sendall(b"Charlie")

    # Receive and decrypt session key
    encrypted_Ks = conn.recv(1024)
    Ks = decrypt_rsa(encrypted_Ks, load_key("CharliePrivateKey.pem"))
    print(f"🔑 Charlie received session key Ks: {Ks}")

    des = DESAlgorithm(Ks)

    # Receive Alice's and Bob's messages
    for _ in range(2):  # Expecting messages from Alice and Bob
        encrypted_msg = conn.recv(1024)
        decrypted_msg = des.decrypt(encrypted_msg).decode()
        print(f"📩 {decrypted_msg}")

    # Now Charlie sends his message
    msg = input("📩 Charlie, enter your message: ")
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    encrypted_msg = des.encrypt(msg.encode())

    conn.sendall(encrypted_msg)

charlie()
