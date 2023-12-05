import socket
import threading

HOST = "127.0.0.1"
PORT = 12343


def receive_messages(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break


def send_messages(s, username):
    while True:
        message = input()
        if message.lower() == "/exit":
            break
        full_message = f"{message}"
        s.sendall(full_message.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    username = input("Enter your name: ")
    s.sendall(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    print(f"PREVED MEDVED, {username}!")

    send_thread = threading.Thread(target=send_messages, args=(s, username))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    print("Exiting the chat.")
