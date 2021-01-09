import socket
import time
import json
import colorama

colorama.init()

TIME_SLEEP = 60


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


class Service_Advertiser:
    username = ""
    UDP_PORT = 5000
    UDP_IP = ''
    IP = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.UDP_IP = self.IP[:10] + "255"
        print(color.YELLOW + "Broadcasting to :" + self.UDP_IP + color.END)
        self.username = self.get_username()

    def send(self, message):
        self.sock.sendto(bytes(message, "utf-8"), (self.UDP_IP, self.UDP_PORT))

    def get_username(self):
        print(color.BOLD + color.RED + "Type Your Username and Press ENTER\n" + color.END)
        user = input()
        return user

    def json_message(self):
        info = {"username": self.username, "ip_address": self.IP}
        jsn = json.dumps(info)
        return jsn


if __name__ == '__main__':
    SerAd = Service_Advertiser()
    message = SerAd.json_message()
    while 1:
        SerAd.send(message)
        print(message + " sent.")
        time.sleep(TIME_SLEEP)
