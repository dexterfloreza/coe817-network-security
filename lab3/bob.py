import socket
import os
from rsa_utils import load_key, encrypt_rsa, decrypt_rsa, generate_key_pair, save_key
from DES import DESAlgorithm

# 🔹 Check if Bob's keys exist, if not, generate them
if not os.path.exists("BobPrivateKey.pem") or not os.path.exists("BobPublicKey.pem"):
    print("🔑 Bob's keys not found! Generating new RSA key pair...")
    BOB_PUBLIC_KEY, BOB_PRIVATE_KEY = generate_key_pair()
    save_key("BobPublicKey.pem", BOB_PUBLIC_KEY)
    save_key("BobPrivateKey.pem", BOB_PRIVATE_KEY)
    print("✅ Bob's RSA keys generated and saved!")

def bob():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 4888))

    conn.sendall(b"Bob")

    # Step 1: Receive encrypted nonce
    encrypted_nonce = conn.recv(1024)
    nonce_and_ida = decrypt_rsa(encrypted_nonce, load_key("BobPrivateKey.pem"))
    N2 = nonce_and_ida[:8]
    ID_A = nonce_and_ida[8:].decode()
    print(f"Bob received Nonce: {N2}, ID_A: {ID_A}")

    # Step 2: Encrypt and return nonce
    conn.sendall(encrypt_rsa(N2, load_key("KDCPrivateKey.pem")))

    # Step 3: Receive and decrypt session key K_B
    encrypted_KB = conn.recv(1024)
    K_B = decrypt_rsa(encrypted_KB, load_key("BobPrivateKey.pem"))
    print(f"Bob decrypted K_B: {K_B}")

    # Step 4: Receive K_AB
    encrypted_KAB = conn.recv(1024)
    des_B = DESAlgorithm(K_B)
    K_AB = des_B.decrypt(encrypted_KAB)[:8]
    print(f"Bob received session key K_AB: {K_AB}")

    # Messaging loop
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5000))
    server.listen(1)
    
    while True:
        conn_alice, _ = server.accept()
        encrypted_msg = conn_alice.recv(1024)
        des_session = DESAlgorithm(K_AB)
        decrypted_msg = des_session.decrypt(encrypted_msg).decode()
        print(f"Message from Alice: {decrypted_msg}")
        conn_alice.close()

bob()
