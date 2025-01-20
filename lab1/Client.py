# Project 1 
# Server to handle one client 
# Create a socket object
import socket
import sys
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Connect to the server
client_socket.connect(server_address)

# Vigenere key
vigenere_key = "TMU"

def main():
    if len(sys.argv) != 3: # point is to make sure user does not provide more than the required arguments 
        print("Usage: python Client.py <host name> <port number>")
        sys.exit(1)
    
    host_name = sys.argv[1]
    try:
        # Creating connection with server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))
            
            print("Connected to server. Type your messages: ")
            
        while True:
            
            user_input = input()
            if not user_input:
                break
        
        client_socket.sendall(user_input.encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8')
        print(f"client: {response}")
        
    except socket.gaierror:
        print(f"Do not know about host {host_name}")
        sys.exit(1)
    
    except ConnectionRefusedError:
        print(f"Could not connect to {host_name} on port {12345}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()
