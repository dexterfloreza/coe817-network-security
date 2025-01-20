import socket
import threading
from vigenere_cipher import VigenereCipher

# Define server address and port
server_address = ('localhost', 12345)

# Initialize Vigenère cipher
vigenere_key = "TMU"
cipher = VigenereCipher(vigenere_key)

# Function to handle a client connection
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            # Receive encrypted message from client
            encrypted_message = client_socket.recv(1024).decode()
            if not encrypted_message:
                print(f"Client {client_address} disconnected.")
                break

            print(f"Received Encrypted Message from {client_address}: {encrypted_message}")

            # Decrypt and display the message
            decrypted_message = cipher.decrypt(encrypted_message)
            print(f"Decrypted Message from {client_address}: {decrypted_message}")

            # Get server's response
            response = input("Enter Server Response: ")
            encrypted_response = cipher.encrypt(response)

            # Send encrypted response to client
            client_socket.send(encrypted_response.encode())
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")

# Main server code
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)  # Allow up to 5 pending connections
    print('Server is listening for connections...')

    try:
        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        server_socket.close()

# Run the server
if __name__ == "__main__":
    start_server()
