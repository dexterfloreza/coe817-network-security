# COE817 LAB 1 Programming with Sockets in Python

## Description

In this lab, we:
- Familiarized ourselves with Python socket programming
- Worked on an implementation of the Vigenere Cipher, the system for encoding and decoding text messages that was discussed in class.

In Project 1, we developed a server that could handle one client and encrypt/decrypt messages transmitted between the client and server through the Vigenere Cipher. Project 2 expands on this by handling multiple clients. 
## Questions and Answers

## How could our server program handle multiple clients? 
Our server program handles multiple clients by using multithreading. Each client connection is handled in a separate thread, allowing the server to manage multiple clients concurrently. 

First, our server listens for incoming client connections using:
```python
server_socket.listen(5)
```
This allows the server to accept up to 5 pending connections simultaneously. The number "5" was chosen arbitrarily, and any number could have been typed here.

Then, when a client connects, the server accepts the connection. This creates a dedicated client_socket for communication with the specific client.
```python
client_socket, client_address = server_socket.accept()
```

After that, for each new client, the server starts a new thread to handle that client. 
```python
client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
client_thread.start()
```
When the function is run in a thread ```threading.Thread```, multiple clients can be handled independently. Each thread runs its own instance of ```handle_client``` for a specific client, ensuring isolated and concurrent communication. 

```target = handle_client:``` this specifies the function (```handle_client```) that will handle communication with the client. 

```args=(client_socket, client_address)``` passes the client-specific socket and address to the handle_client function. 

The handle_client function processes messages from individual clients. 
```python
def handle_client(client_socket, client_address):
    while True:
        encrypted_message = client_socket.recv(1024).decode()
        decrypted_message = cipher.decrypt(encrypted_message)
        response = input("Enter Server Response: ")
        encrypted_response = cipher.encrypt(response)
        client_socket.send(encrypted_response.encode())
```
Inside this function, the server receives message from the client in the first line, with the argument 1024 specifying the maximum buffer size for the incoming data. In this case, the server can read up to 1024 bytes in a single operation. Then, it decrypts them, and displays them. Then, it waits for input from the server operator, encrypts the response, and sends it back to the client. If the client disconnects, the function ends, and the thread effectively terminates. 

## Where did you encrypt chat messages in your program?

Every messages sent between the client and server is encrypted before transmission and decrypted upon receipt. Both the client and the server use the same shared Vigenere cipher key (```vigenere_key = "TMU"```) to encrypt and decrypt messages, ensuring secure communication.  

# Encryption on the Client Side
When the client sends a message to the server, the client first encrypts the message using the Vigenere cipher before sending it. This happens in the following lines: 
```python
# Encrypt and send the message
encrypted_message = cipher.encrypt(message)  # Message encryption
client_socket.send(encrypted_message.encode())  # Sending the encrypted message
```
The purpose of this is that the plain-text message typed by the user is encrypted using the shared key before being sent to the server. This ensures that the message remains secure while being transmitted over the network. 


# Encryption on the Server Side
When the server responds to the client, it encrypts the server operator's response before sending it to the client. This happens in the following lines:
```python
# Get server's response and encrypt it
response = input("Enter Server Response: ")  # Server operator's plain-text response
encrypted_response = cipher.encrypt(response)  # Encrypting the response
client_socket.send(encrypted_response.encode())  # Sending the encrypted response
```

This encrypts its response to ensure that only the client (who has the shared key) can decrypt and read the message. 

## Where did you decrypt chat messages in your program? 
# Decryption on the Client Side
When the client receives a response from the server, it decrypts the encrypted response to retrieve the original plain text. This happens in the following lines of code:

```python
# Receive and decrypt server response
encrypted_response = client_socket.recv(1024).decode()  # Receive and decode
decrypted_response = cipher.decrypt(encrypted_response)  # Decrypt the response
print(f"Server: {decrypted_response}")  # Display the plain-text response
```

Here, the client decrypts the server's response using the shared key, allowing the user to read the original message sent by the server. 

# Decryption on the Server Side 
When the server receives the encrypted message from the client, it decrypts the message using the Vigenere cipher to retrieve the original plain text. This happens in the following lines of the server.py code: 
```python
# Receive encrypted message from client
encrypted_message = client_socket.recv(1024).decode()  # Receive and decode
decrypted_message = cipher.decrypt(encrypted_message)  # Decrypt the message
```
The server decrypts the incoming encrypted message using the same shared key. This allows the server operator to read the original message sent by the client. 
