import socket
from vigenere_cipher import VigenereCipher

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Bind the socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print('Waiting for a connection...')

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address}')


# Initialize Vigenère cipher
vigenere_key = "TMU"
cipher = VigenereCipher(vigenere_key)

try:
    while True:
        # Receive encrypted message from client
        encrypted_message = client_socket.recv(1024).decode()
        if not encrypted_message:
            print(f"NOT ENCRYPTED")
            break
        print(f"Received Encrypted Message: {encrypted_message}")
        print(f"")

        # Decrypt and display the message
        decrypted_message = cipher.decrypt(encrypted_message)
        print(f"Decrypted Message: {decrypted_message}")
        print(f"")

        # Get server's response
        response = input("Enter Server Response: ")
        encrypted_response = cipher.encrypt(response)

        # Send encrypted response to client
        client_socket.send(encrypted_response.encode())
finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
