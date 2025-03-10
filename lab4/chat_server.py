import socket
import threading
import datetime
from DES import DESAlgorithm

clients = []

# Broadcast messages to all clients except sender
def broadcast(message, sender_conn):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Timestamp format
    for client in clients:
        if client != sender_conn:  # Don't send back to sender
            try:
                client.sendall(message)
            except Exception as e:
                print(f"❌ Error sending message: {e}")

# Handle each connected client
def handle_client(conn, Ks):
    des = DESAlgorithm(Ks)
    while True:
        try:
            encrypted_msg = conn.recv(1024)
            if not encrypted_msg:
                break

            decrypted_msg = des.decrypt(encrypted_msg).decode()
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Get timestamp
            print(f"📩 {timestamp} Received: {decrypted_msg}")

            # Append timestamp and forward to all clients
            encrypted_msg_with_timestamp = des.encrypt(f"{timestamp} {decrypted_msg}".encode())
            broadcast(encrypted_msg_with_timestamp, conn)

        except Exception as e:
            print(f"❌ Connection error: {e}")
            break

    conn.close()
    clients.remove(conn)

# Start the chat server
def start_chat_server(Ks):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5001))
    server.listen(5)
    print("🚀 Chat server is running on port 5001...")

    while True:
        conn, addr = server.accept()
        print(f"🔗 New client connected: {addr}")
        clients.append(conn)

        threading.Thread(target=handle_client, args=(conn, Ks)).start()
