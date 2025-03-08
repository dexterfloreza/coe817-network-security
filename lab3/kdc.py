import socket
import os
from rsa_utils import load_key, encrypt_rsa, decrypt_rsa
from DES import DESAlgorithm

def start_kdc():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 4888))
    server.listen(2)
    print("KDC is listening on port 4888...")

    conn_a, addr_a = server.accept()
    print(f"Connected to Alice: {addr_a}")
    ida = conn_a.recv(1024).decode().strip()

    conn_b, addr_b = server.accept()
    print(f"Connected to Bob: {addr_b}")
    idb = conn_b.recv(1024).decode().strip()

    # Generate nonces
    N1 = os.urandom(8)
    N2 = os.urandom(8)

    # Step 1: Send nonces to Alice & Bob
    conn_a.sendall(encrypt_rsa(N1 + idb.encode(), load_key("AlicePublicKey.pem")))
    conn_b.sendall(encrypt_rsa(N2 + ida.encode(), load_key("BobPublicKey.pem")))

    # Step 2: Receive and verify nonces
    encrypted_response_a = conn_a.recv(1024)
    decrypted_NA_N1 = decrypt_rsa(encrypted_response_a, load_key("KDCPrivateKey.pem"))
    
    encrypted_response_b = conn_b.recv(1024)
    decrypted_NB_N2 = decrypt_rsa(encrypted_response_b, load_key("KDCPrivateKey.pem"))

    if decrypted_NA_N1[:8] != N1 or decrypted_NB_N2[:8] != N2:
        print("Nonce verification failed! Closing connections.")
        conn_a.close()
        conn_b.close()
        return

    # Step 3: Send session keys K_A and K_B
    K_A = os.urandom(8)
    K_B = os.urandom(8)
    
    conn_a.sendall(encrypt_rsa(K_A, load_key("AlicePublicKey.pem")))
    conn_b.sendall(encrypt_rsa(K_B, load_key("BobPublicKey.pem")))

    # Generate shared session key K_AB
    K_AB = os.urandom(8)
    
    # Encrypt K_AB with K_A and K_B
    des_A = DESAlgorithm(K_A)
    encrypted_K_AB_A = des_A.encrypt(K_AB + idb.encode())
    conn_a.sendall(encrypted_K_AB_A)

    des_B = DESAlgorithm(K_B)
    encrypted_K_AB_B = des_B.encrypt(K_AB + ida.encode())
    conn_b.sendall(encrypted_K_AB_B)

    print("Key distribution completed. Alice and Bob can now securely communicate.")
    
    conn_a.close()
    conn_b.close()

start_kdc()
