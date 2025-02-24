# COE817 LAB 3 

## Description

In this lab, we implemented a hybrid key distribution protocol which consists of two phases: a public-key scheme used to distribute a master key and then a server generating a session key.

## Lab Demo

# Summary of Workflow
1. KDC (Server) listens for connections from Alice and Bob.
2. Alice & Bob each send their ID (```IDA```, ```IDB```) to the KDC.
3. KDC generates random nonces (```N1```, ```N2```) and sends them encrypted to Alice & Bob.
4. Alice & Bob decrypt the nonces, encrypt them with KDC’s public key, and send them back.
5. KDC verifies the nonces to confirm their identities.
6. KDC generates two session keys (```K_A``` for Alice, ```K_B``` for Bob).
7. KDC securely distributes a shared session key (```K_AB```) to Alice & Bob.
8. Alice and Bob can now securely communicate using ```K_AB```.

First, the KDC acts as a server using Python's socket module. It binds to local host on port 4888 and listens for connections. First, Alice connects, then Bob.
```server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 4888))
server.listen(2)  # Waits for connections from Alice & Bob```

Secondly, Alice and Bob send their identifiers ```IDA``` and ```IDB``` and then KDC receives their IDs and stores them. This is found in the following code:

```conn_a, addr_a = server.accept()
ida = conn_a.recv(1024).decode().strip()

conn_b, addr_b = server.accept()
idb = conn_b.recv(1024).decode().strip()
```

Thirdly, KDC encrypts each nonce using Alice's and Bob's public keys and sends them. 
```
N1 = os.urandom(8)  # Random 8-byte nonce for Alice
N2 = os.urandom(8)  # Random 8-byte nonce for Bob

conn_a.sendall(encrypt_rsa(N1 + idb.encode(), load_key("AlicePublicKey.pem")))
conn_b.sendall(encrypt_rsa(N2 + ida.encode(), load_key("BobPublicKey.pem")))
```

Fourthly, Alice and Bob decrypt their respective nonces using their private keys. They re-encrypt them using KDC's public key and send them back. 

```encrypted_response_a = conn_a.recv(1024)
decrypted_NA_N1 = decrypt_rsa(encrypted_response_a, load_key("KDCPrivateKey.pem"))
```
KDC then checks if the receive nonce matches the original N2 nad N2 to verify identity.

After that, KDC generates and sessions keys ```K_A``` and ```K_B```. If the nonce verificatin is succesful, KDC generates Alice's session key, Bob's session key, and the shared session key, ```K_AB.```

```K_A = os.urandom(8)  # Alice's session key
K_B = os.urandom(8)  # Bob's session key
K_AB = os.urandom(8) # Shared session key
```

KDC also encrypts ```K_A``` and ```K_B``` for Bob.

```
conn_a.sendall(encrypt_rsa(K_A, load_key("AlicePublicKey.pem")))
conn_b.sendall(encrypt_rsa(K_B, load_key("BobPublicKey.pem")))
```

In the sixth step, KDC encrypts and sends ```K_AB``` using ```K_A``` and ```K_B``` before sending to Bob.
Once this is complete, Alice and Bob can decrypt ```K_AB``` and communicate securely. 

```
des_A = DESAlgorithm(K_A)
encrypted_K_AB_A = des_A.encrypt(K_AB + idb.encode())  # Encrypt K_AB for Alice
conn_a.sendall(encrypted_K_AB_A)

des_B = DESAlgorithm(K_B)
encrypted_K_AB_B = des_B.encrypt(K_AB + ida.encode())  # Encrypt K_AB for Bob
conn_b.sendall(encrypted_K_AB_B)
```

# Public and Private Key Pairs of A, B and the server
The public and private key pairs of A, B, and the server are kept in files detailed below.

Summary: 
- Alice's Public Key (for Encryption): AlicePublicKey.pem
- Alice's Private Key (for Decryption): AlicePrivateKey.pem
- Bob's Public Key (for Encryption): BobPublicKey.pem
- Bob's Private Key (for Decryption): BobPrivateKey.pem
- KDC(server)'s Public Key (for Encryption): KDCPublicKey.pem
- KDC(server)'s Private Key (for Decryption): KDCPrivateKey.pem

Alice and Bob sends each other encrypted messaged to KDC using its public key (KDCPublicKey.pem).

Alice encrypts her nonce using KDCPublicKey.pem, and then KDC decrypts it using its private key KDCPrivateKey.pem.

KDC then encrypts each session's keys (K_A, K_B) using Alice's and Bob's public keys.
Alice then decrypts is using AlicePrivateKey.pem 

Alice and Bob then encrypt messages using their shared session key (K_AB). They don't use RSA for this step, but instead use DES encryption. 

# The decrypted KA and KB
The decrypted KA should look something like:
```b'\xd4\xe2t\xbb\x10Q\x11\x7f'```

The decrypted KB should look something like:
``` b'\x18C)\xd0?o4\xb1'```

In other words, they should not be the same. They should be unique, because in the hybrid key distribution protocol, K_A and K_B are separate keys given to Alice and Bob respectively. The unique value of each key ensures the security of them. 

# Demonstrate if both A and B could correctly receive the same K_AB from the server. Explain your code and tell how your server socket program makes it work. The protocol is vulnerable. Why? How to solve the problem? 
In Phase 2 of the code, it appears that both Alice and Bob can correctly receive the same K_AB from the server. That value should look like: 
```b'\x99\x9e\xef\xd4\xb1\xd6e\xf0'```

The way the server socket program, KDC, makes it work is that KDC starts a server socket with the following code: 
```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 4888))  # Binds to port 4888
server.listen(2)  # Listen for up to 2 clients (Alice and Bob)
print("KDC is listening on port 4888...")
```

Basically, the server waits for Alice and Bob to connect and then ```server..listen(2)``` allows up to 2 clients to connect at the same time.

Then Alice connects first, then Bob connects. The KDC server then accepts their connetions retrieves their identifiers.

```
conn_a, addr_a = server.accept()
print(f"Connected to Alice: {addr_a}")
ida = conn_a.recv(1024).decode().strip()  # Receives Alice's ID

conn_b, addr_b = server.accept()
print(f"Connected to Bob: {addr_b}")
idb = conn_b.recv(1024).decode().strip()  # Receives Bob's ID
```

server.accepts() blocks execution until Alice/Bob connect, then recv(1024) receives Alice's and BOb's IDs and then the server now knows Alice and BOb ar ready to exchange keys.

After that, KDC generates random 8-byte nonces N1 and N2 in the code below. This ensures that Alice and Bob are communicating with the real KDC. The nonces also prevent replay attacks and are encrypted so that only Alice/Bob can decrypt them. 
```
N1 = os.urandom(8)  # Random nonce for Alice
N2 = os.urandom(8)  # Random nonce for Bob

conn_a.sendall(encrypt_rsa(N1 + idb.encode(), load_key("AlicePublicKey.pem")))
conn_b.sendall(encrypt_rsa(N2 + ida.encode(), load_key("BobPublicKey.pem")))
```

Then, Alice and Bob decrypt their nonces and send them back, encrypted with the KDC's public key. KDC decrypts and verifies if the received nonce matches the original. Basically checks if they match the nonces, and if so, they're authenticated. 
```
encrypted_response_a = conn_a.recv(1024)
decrypted_NA_N1 = decrypt_rsa(encrypted_response_a, load_key("KDCPrivateKey.pem"))

encrypted_response_b = conn_b.recv(1024)
decrypted_NB_N2 = decrypt_rsa(encrypted_response_b, load_key("KDCPrivateKey.pem"))

if decrypted_NA_N1[:8] != N1 or decrypted_NB_N2[:8] != N2:
    print("Nonce verification failed! Closing connections.")
    conn_a.close()
    conn_b.close()
    return
```

Afterwards, KDC then generates the session keys K_A, K_B, and the shared session key, K_AB. 
```
K_A = os.urandom(8)  # Alice's session key
K_B = os.urandom(8)  # Bob's session key
K_AB = os.urandom(8) # Shared session key

conn_a.sendall(encrypt_rsa(K_A, load_key("AlicePublicKey.pem")))
conn_b.sendall(encrypt_rsa(K_B, load_key("BobPublicKey.pem")))

```

Finally, the share dsession key is used for encrypted commuincation between Alice and Bob in the code below, with each K value being encrypted separately.
```
des_A = DESAlgorithm(K_A)
encrypted_K_AB_A = des_A.encrypt(K_AB + idb.encode())  # Encrypt K_AB for Alice
conn_a.sendall(encrypted_K_AB_A)

des_B = DESAlgorithm(K_B)
encrypted_K_AB_B = des_B.encrypt(K_AB + ida.encode())  # Encrypt K_AB for Bob
conn_b.sendall(encrypted_K_AB_B)
```
Alice decrypts K_AB using K_A, and vice versa with Bob. Then, Alice and Bob can communicate securely using K_AB.

Once the key distribution is complete, KDC then closes the connections.
```
conn_a.close()
conn_b.close()
print("Key distribution completed. Alice and Bob can now securely communicate.")
```
This ensures that all data is sent before clsoing the connectoins and then KDC finishes its role and then Alice and Bob can takeover comunications.



Some of the vulnerabilities and security issues with this somewhat secure protocol is that it is vulnerable to the man-in-the-middle (MITM) attack. If an attacker intercepts the connection between Alice/Bob and the KDC they can then modify the messages. For example, a hacker could replace ```K_AB``` with their own session key, effectively engaging in identity theft and impersonating the server. To solve this, you can use mutual authentication where both Alice and Bob verify KDC's identity and implement digital signatures to ensure that each client is who they claim to be. 

Furthermore, if an attacker records encrypted messages, they can replay them later to impersonate Alice or Bob. To solve this, one possible solution includes including timestamps in the messages and usin session-based tokens that expire after use, instead of using the same tokens over and over again. 

