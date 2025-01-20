# COE817 LAB 1

COE817 Lab 1. 
## Description

In this lab, we:
- Familiarized ourselves with Python socket programming
- Worked on an implementation of the Vigenere Cipher, the system for encoding and decoding text messages that was discussed in class.

In Project 1, we developed a server that could handle one client and encrypt/decrypt messages transmitted between the client and server through the Vigenere Cipher. Project 2 expands on this by handling multiple clients. 
## Getting Started

### Answers to Questions 
## How could our server program handle multiple clients? 
Our server program handles multiple clients by using multithreading. Each client connection is handled in a separate thread, allowing the server to manage multiple clients concurrently. 

```python
client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
client_thread.start()

The handle_client function processes messages from individual clients. 
def handle_client(client_socket, client_address):
    while True:
        encrypted_message = client_socket.recv(1024).decode()
        decrypted_message = cipher.decrypt(encrypted_message)
        response = input("Enter Server Response: ")
        encrypted_response = cipher.encrypt(response)
        client_socket.send(encrypted_response.encode())
```
