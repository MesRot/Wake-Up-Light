from bluetooth import *
import datetime


def send_message(message):
    bg_addr = '64:80:99:B0:77:A9'
    port = 1
    try:
        sock = BluetoothSocket(RFCOMM)
        sock.connect((bg_addr, port))
        sock.send(message)
        sock.close()
    except BluetoothError as e:
        print(f"Sending message failed {e}")


def set_alarm(alarm_date):
    alarm_date = alarm_date.strftime("%m/%d/%Y, %H:%M:%S")
    message = f"ALARM & {alarm_date}"
    send_message(message)


def main():
    send_message("Fanni on ihana")


if __name__ == "__main__":
    main()
    #set_alarm(datetime.datetime.now())
















