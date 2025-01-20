import socket
from vigenere_cipher import VigenereCipher

# Define server address and port
server_address = ('localhost', 12345)

# Initialize Vigenère cipher
vigenere_key = "TMU"
cipher = VigenereCipher(vigenere_key)

try:
    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        print("Connected to server. Type your messages:")

        while True:
            # Get user input
            message = input("You: ")
            if not message:
                break

            # Encrypt the message
            encrypted_message = cipher.encrypt(message)
            print(f"Encrypted Message Sent: {encrypted_message}")  # Display encrypted message
            print(f"")

            # Send the encrypted message
            client_socket.send(encrypted_message.encode())

            # Receive the encrypted response from the server
            encrypted_response = client_socket.recv(1024).decode()
            if not encrypted_response:
                break
            print(f"Encrypted Server Message Received: {encrypted_response}")  # Display encrypted response
            print(f"")
            
            # Decrypt the response
            decrypted_response = cipher.decrypt(encrypted_response)
            print(f"Decrypted Server Message Received: {decrypted_response}")  # Display decrypted message
            print(f"")

except ConnectionRefusedError:
    print("Connection refused. Ensure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
