import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12343

clients = set()


def broadcast(message, sender_socket, sender_username):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    full_message = f"[{timestamp}] {sender_username}: {message}"

    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(full_message.encode())
            except:
                remove_client(client)


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()


def handle_client(client_socket):
    with client_socket:
        username = client_socket.recv(1024).decode()
        clients.add(client_socket)
        print(f"New connection from {username}")
        broadcast(f"{username} joined the chat.", client_socket, "Server")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received {data.decode()} from {username}")
                broadcast(data.decode(), client_socket, username)
            except:
                remove_client(client_socket)
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()

        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()
