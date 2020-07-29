import sqlite3

from bluetooth import *
import socket


DEFAULT_PATH =  "alarms.db"


def process(message):
    command, text = message.split("&").strip()
    if command == "ALARM":
        write_to_sql(text)
    pass


def run_server():
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
                viesti = data.decode("utf-8")
                process(viesti)
            except BluetoothError as e:
                break
            if not data:
                break
            total += len(data)
            print(f"Total byte read: {total}")

        client_sock.close()
        print("Connection closed")
    server_sock.close()


def db_connect(db_path=DEFAULT_PATH):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except:
        print("Failed to get connection")
    return conn


def write_to_sql(message):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS alarms")
    cur.execute("CREATE TABLE alarms(time text)")
    cur.execute('''INSERT INTO alarms VALUES(?)''', (message,) )
    conn.commit()
    conn.close()


def main():
    run_server()


if __name__ == "__main__":
    main()













