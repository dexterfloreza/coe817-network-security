import socket
from rsa_utils import load_key, encrypt_rsa, decrypt_rsa
from DES import DESAlgorithm

def alice():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 4888))

    conn.sendall(b"Alice")

    # Step 1: Receive encrypted nonce
    encrypted_nonce = conn.recv(1024)
    nonce_and_idb = decrypt_rsa(encrypted_nonce, load_key("AlicePrivateKey.pem"))
    N1 = nonce_and_idb[:8]
    ID_B = nonce_and_idb[8:].decode()
    print(f"Alice received Nonce: {N1}, ID_B: {ID_B}")

    # Step 2: Encrypt and return nonce
    conn.sendall(encrypt_rsa(N1, load_key("KDCPrivateKey.pem")))

    # Step 3: Receive and decrypt session key K_A
    encrypted_KA = conn.recv(1024)
    K_A = decrypt_rsa(encrypted_KA, load_key("AlicePrivateKey.pem"))
    print(f"Alice decrypted K_A: {K_A}")

    # Step 4: Receive K_AB
    encrypted_KAB = conn.recv(1024)
    des_A = DESAlgorithm(K_A)
    K_AB = des_A.decrypt(encrypted_KAB)[:8]
    print(f"Alice received session key K_AB: {K_AB}")

    # Messaging loop
    while True:
        msg = input("Enter message to send to Bob: ")
        des_session = DESAlgorithm(K_AB)
        encrypted_msg = des_session.encrypt(msg.encode())

        # Send message to Bob
        conn_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_bob.connect(("localhost", 5000))
        conn_bob.sendall(encrypted_msg)
        conn_bob.close()

alice()
