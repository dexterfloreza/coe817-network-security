# COE817 LAB 1

COE817 Lab 1. 
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


