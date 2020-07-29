from bluetooth import *

bg_addr = '00:1A:7D:DA:71:13'

port = 1

sock = BluetoothSocket(RFCOMM)

sock.connect((bg_addr, port))

sock.send("Hello word!")

sock.close()
















