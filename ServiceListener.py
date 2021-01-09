import socket
import json
import colorama
import time
import threading

colorama.init()


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Service_Listener:
    UDP_PORT = 5000
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    baglantilar = dict()
    baglantilar_ters = dict()

    def __init__(self):
        self.listen_sock.bind(('', self.UDP_PORT))
        print(color.BOLD + color.BLUE + "Listening..." + color.END)

    def receive(self):
        data, addr = self.listen_sock.recvfrom(1024)
        return (data, addr)


if __name__ == '__main__':
    SerLis = Service_Listener()
    while True:
        while True:
            data, addr = SerLis.receive()  # buffer size is 1024 bytes
            message_str = str(data, 'utf-8')
            print(color.UNDERLINE + color.RED + ".JSONDecodeError:" + color.END)
            time.sleep(1)
            info = json.loads(message_str)
            try:
                print(color.BOLD + color.GREEN + info["username"] + " is online." + color.END)
                SerLis.baglantilar[info["username"]] = addr[0]
                SerLis.baglantilar_ters[addr[0]] = info["username"]

                with open('Peers.txt', 'w') as tum_baglantilar:
                    json.dump(SerLis.baglantilar, tum_baglantilar)

                with open('Peers_ters.txt', 'w') as tum_baglantilar:
                    json.dump(SerLis.baglantilar_ters, tum_baglantilar)

            except KeyError:
                print(color.UNDERLINE + color.RED + "Key is not usable. Use keys: {"+"username"+":"+", ip_address"+": "+"} " + color.END)
                time.sleep(1)

