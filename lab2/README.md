# COE817 LAB 2 Python Cryptography and Authentication Protocols

## Description

In this lab, we familiarized ourselves with various authentication protocols and Python cryptography libraries. 

## Questions and Answers

## For Project 1, show the following messages: the received messsage 1, the received message 2, the decrypted message 2, the received message 3, the decrypted message 3

The project implements a symmetric key-based authentication protocol using DES encryption. The communication follows these three steps:

1. Alice sends her ID and a nonce to Bob.
2. Bob responds with a new nonce and an encrypted version of Alice's nonce + Bob's ID.
3. Alice verifies the response, encrypts Bob's nonce, and sends it back to Bob.

```KEY = b'8bytekey' ``` is the symmetric key used for encryption and decryption. Both Alice and Bob use the same key.

This code provides the necessary padding because DES requires input data in multiples of 8 bytes.
```
# Function to pad data to be a multiple of 8 bytes
def pad(data):
    while len(data) % 8 != 0:
        data += " "  # Pad with spaces
    return data
```

Then, a DES cipher is created and then we pad the message so that its length is a multiple of 8.
After that, it encrypts the message and then encodes it in Base64 (to make it easily transferable as a string). After that, our code decodes Base64, decrypts using DES, removes padding, and then returns the plaintext message.

Received Message: ```Bob received: ID_A = A, Nonce_A = 1234```

Received Message 2: ```[Alice Received Response: {"ID": "B", "Nonce": "1234"}```

Decrypted Message 2: ```[Alice Received Response: {"ID": "B", "Nonce": "1234"}```

Received Message 3: ```Bob received decrypted: "ID": "A", "Nonce": "5678"}```

Decrypted Message 3:  ```Bob received decrypted: {"ID": "A", "Nonce": "5678"}```

For Alice, Alice has a fixed ID ("A") and a nonce ("1234").
```    def initiate_communication(self, bob_host, bob_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("[Alice] Connecting to Bob...")
                s.connect((bob_host, bob_port))
                print("[Alice] Connected!")
```

Alice then creates a socket and connects to Bob's server.
```                message_1 = json.dumps({"ID": self.ID_A, "Nonce": self.nonce_A})
                s.sendall(message_1.encode())
                print(f"[Alice] Sent: {message_1}")
```

Alice sends her ID and nonce to Bob.
```                response_1 = s.recv(1024).decode()
                response_data = json.loads(response_1)
                nonce_B = response_data["Nonce_B"]
                encrypted_data = response_data["Encrypted"]
```

Alice then receives Bob's response, which includes Bob's nonce (nonce_B) and an encrypted message that should contain Alice's nonce and bob's ID. 
```
                decrypted_data = decrypt_message(encrypted_data)
                print(f"[Alice] Decrypted response: {decrypted_data}")
```

Alice then decrypts the message from Bob to verify her nonce is included.
```                encrypted_final = encrypt_message(json.dumps({"ID": self.ID_A, "Nonce": nonce_B}))
                s.sendall(encrypted_final.encode())
                print(f"[Alice] Sent encrypted final message: {encrypted_final}")
```


Alice encrypts Bob's nonce and then sends it back to Bob for verification.

On Bob's side (the server side), Bob has a fixed ID ("B")

```     def start_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("Bob is listening for Alice...")
            conn, addr = s.accept()
```

And then creates a server socket and waits for Alice to connect. 
```                request_1 = conn.recv(1024).decode()
                request_data = json.loads(request_1)
                nonce_A = request_data["Nonce"]
                print(f"Bob received: ID_A={request_data['ID']}, Nonce_A={nonce_A}")
```

Bob then receives Alice's message, extracting Alice's ID and Alice's nonce (nonce_A).
```                nonce_B = "5678"  # Bob's random nonce
                encrypted_message = encrypt_message(json.dumps({"ID": self.ID_B, "Nonce": nonce_A}))
```

Bob then generates his own nonce, nonce_B = "5768". Bob also encrypts a message containing Alice's nonce and Bob's ID.
```                response = json.dumps({"Nonce_B": nonce_B, "Encrypted": encrypted_message})
                conn.sendall(response.encode())
                print(f"Bob sent: Nonce_B={nonce_B}, Encrypted={encrypted_message}")
```

After that, Bob receives Alice's final encrypted response and decrypts it. If the message contains his nonce (nonce_B), then Bob authenticates Alice successfully.

The execution follow can be summarized as follows:

1. Alice → Sends {"ID": "A", "Nonce": "1234"} to Bob.
2. Bob → Generates a new nonce "5678", encrypts {"ID": "B", "Nonce": "1234"} (which contains Alice's nonce).
3. Alice → Decrypts Bob's response to confirm "1234" is inside.
4. Alice → Encrypts Bob’s nonce "5678" and sends it back.
5. Bob → Decrypts Alice’s final response to confirm "5678" is inside.
6. Mutual Authentication Complete ✅.

## For Project 2, show the following messages: the received message 1, the received message 2, the decrypted messsage 2, the received message 3, the decrypted message 3

## For Project 3, explain your revised design of the protocol. Show the received signature of message M. 


