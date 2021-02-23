import socket
import threading
from PImatrix.controller import Controller

# Universe 1
# 0: Mode
# 1: Speed
# 2: Bands
# 3: VU Mode


UNIVERSE_1 = 2
UNIVERSE_2 = 3
UDP_IP = "127.0.0.1"
UDP_PORT = 6454

mode = 0
thread = None
last_seq_1 = 0
last_seq_2 = 0
data = [0] * 630

try:
    controller = Controller()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, address = sock.recvfrom(630)
        print(f"New connection from {address}.")
        if len(data) < 18 or data[9] != 0x50 or data[11] < 14:
            print("Err: Invalid or not supported ArtNet package")
            continue

        universe = data[15] << 8 | data[14]
        sequence = data[12]
        length = int(data[17])
        payload = data[18 : 17 + length]
        if universe == UNIVERSE_2 and last_seq_2 < sequence:
            last_seq_2 = sequence
            controller.set_data(payload, 512)
        elif universe == UNIVERSE_1 and last_seq_1 < sequence:
            last_seq_1 = sequence
            controller.set_data(payload)
            if mode != data[0]:
                mode = data[0]
                if thread is not None:
                    controller.running = False
                    thread.join()
                thread = threading.Thread(target=controller.run)
                thread.start()
finally:
    if thread is not None:
        controller.running = False
        thread.join()
