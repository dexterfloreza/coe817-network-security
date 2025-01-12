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

# Accept a connection
print('Waiting for a connection...')
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address}')
