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
For Project 3, we've implemented:
1. RSA key pair generation (Public/Private Keys)
2. Message signing by Alice using her private key.
3. Signature verification by bob using Alice's public key.
4. Protectoin against replay attacks by including a nonce (timestamp-based) in the signed message.

The code below contains functions for RSA key generation, message signing, and verification.
```from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import time
import json

# Generate RSA key pair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Sign message with Alice's private key
def sign_message(private_key, message):
    key = RSA.import_key(private_key)
    message_bytes = message.encode()
    hashed_message = SHA256.new(message_bytes)
    signature = pkcs1_15.new(key).sign(hashed_message)
    return base64.b64encode(signature).decode()

# Verify signature using Alice's public key
def verify_signature(public_key, message, signature):
    key = RSA.import_key(public_key)
    message_bytes = message.encode()
    hashed_message = SHA256.new(message_bytes)
    try:
        pkcs1_15.new(key).verify(hashed_message, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False
```


Furthermore, we've also updated the authentication protocol such that Bob verifies both the signature and the freshness of the timestamp to prevent replay attacks.

In Alice's script, we have Alice (the client) who generates an RSA key pair, signs a message along with a teimstamp, and then sends the message, timestamp, and signature to Bob.
```
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
```



In Bob's script, Bob receives Alice's signed message, verifies the signature using Alice's public key, and then checks the timestamp to prevent replay attacks.
```
# bob_server.py
import socket
import json
import datetime
from digital_signature import generate_rsa_keys, sign_message

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
```


The original problem was that in the original vulnerable protocol, an atatcker could capture and replace Alice's message to impersonate her. The new solution has the message include a timestamp to track when it was sent, a signature which includes the timestamp soi tcannot be altered, and then Bob must verify it so that the signature is valid (ensuring message authenticity) and that the timestamp is within the last 30 seconds (effectively preventing replay attacks). 

To specify, replay attacks are prevented by including timestamps (a timestamp that's too old would be rejected by Bob) and through nonces (which ensures uniqueness, making it difficult for attackers to manipulate old messages).

This generates a new nonce. 
```nonce = str(random.randint(100000, 999999))  # Generate a random nonce```
Essentially, a nonce is a random six-digit number between 100000 and 999999. Every time Alice (the client) signs a message, a new nonce is generated. This ensures each signed message is unique even if the actual message content M is the same. When Bob receives the message, he checks the nonce and timestamp together to prevent replay attacks.

#Message Signing
```def sign_message(message, private_key):
    timestamp = str(int(time.time()))  # Get current time in seconds
    nonce = str(random.randint(100000, 999999))  # Generate a random nonce
    combined_message = message + nonce + timestamp  # Concatenate M + Nonce + Timestamp
```

#Message Verification (Bob's Side):
```def verify_message(message, nonce, timestamp, signature, public_key):
    combined_message = message + nonce + timestamp  # Reconstruct message
```


