from bluetooth import *
import socket

server_sock = BluetoothSocket(RFCOMM)
port = 1
server_sock.bind(("", port))
server_sock.listen(1)

while True:
    print("Waiting for incoming connection...")

    client_sock, address = server_sock.accept()

    print(f"Accepted connection from {address}")

    print("Waiting for data...")

    total = 0

    while True:
        try:
            data = client_sock.recv(1024)
        except BluetoothError as e:
            break
        if not data:
            break
        total += len(data)
        print(f"Total byte read: {total}")

    client_sock.close()
    print("Connection closed")

server_sock.close()














