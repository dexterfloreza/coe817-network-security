# COE817 LAB 4

## Description

In this lab, we implement a socket communication program to implement a secure chat system by implementing a server (KDC) is needed for distributing session keys to three clients (A, B, and C). 

## Required Security Features
- Authenticated key distribution between KDC and chat clients
- ALL chat messages need to be encrypted using a blcok cipher such as DES or AES. A digitla signature must be appended to all chat messages.
- Solution to combat replay attacks. 

## Lab Demo

# Summary of Workflow Phases

1️⃣ Key Exchange Phase

Alice, Bob, and Charlie connect to KDC.
KDC generates a session key (Ks) and encrypts it using each client’s public key.
Each client receives and decrypts Ks using their private key.

2️⃣ Message Exchange Phase

Clients take turns sending encrypted messages to the KDC.
KDC decrypts the message, timestamps it, and forwards it to the other clients.

3️⃣ Security Measures

DES Encryption ensures messages are protected.
Timestamps help prevent replay attacks by ensuring old messages are not reprocessed.

# KDC (Key Distribution + Message Forwarding)
The KDC:

1. Waits for Alice, Bob, and Charlie to connect.
2. Generates a shared session key (Ks) for encrypted communication.
3. Encrypts Ks using each client’s public key and sends it securely.
4. Manages the message exchange loop:
Waits for a client to send a message.
Decrypts the message.
Adds a timestamp to prevent replay attacks.
Encrypts and forwards the message to the other two clients.

# Clients (Alice, Bob, Charlie)
Each client:

1. Connects to the KDC and requests the session key (Ks).
2. Decrypts Ks using their private key.
3. Takes turns sending messages to the KDC.
4. Receives and decrypts messages forwarded by the KDC.


# Explanation of Code

Your program needs to generate the message of protocol in (1) and display it. Then show TA if the same message M could be received by B and C after decryption and signature verification.

Explain your code and tell how your KDC progfram could successfully forward a message to remainin cients. For example, if a chat messge is from A, your program will ensure that KDC wll forward A's message to B and C only. 

Basically, the following sequence of events is followed to successfully forward messages to clients.

If Alice sends a message:

The KDC decrypts Alice’s message.
The KDC adds a timestamp to prevent replay attacks.
The KDC encrypts the message again.
The KDC sends the message to Bob and Charlie ONLY.
Alice does NOT receive her own message.
This process is repeated when Bob and Charlie send messages.


# Demo your improved protocol and show how your solution could resist replay attack. 
To resist replay attacks, timestamps are added to each message at the KDC level. The receiving clients verify the timestamps before processing messages. This works because if an attacker captures a message and tries to resend it, then the tiemstamp will reveal it as an old message, effectively preventing message duplication attacks.

