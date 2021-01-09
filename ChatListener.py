import socket
import threading
import json
import datetime
import time
import colorama

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


PORT=5001


class Listener:
    time_started = 0
    baglantilar = []
    baglantilar_ters=[]
    chat_log=[]
    def __init__(self):
        self.time_started = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('',PORT))
        sock.listen(1)
        print(color.BOLD+color.GREEN+"Connected to socket...")
        print("Waiting for connections...\n"+color.END)
        while True:
            self.update_users()
            musteri, adresi = sock.accept()
            paralel_islem = threading.Thread(target=self.listen_to_given_socket, args=(musteri, adresi))
            paralel_islem.daemon = True
            paralel_islem.start()

    def update_users(self):
        try :
            with open('Peers_ters.txt', 'r') as tum_baglantilar:
                try:
                    self.baglantilar_ters = json.load(tum_baglantilar)
                except:
                    print(color.BOLD+color.BLUE+"Dictionary is empty."+color.END)

            with open('Peers.txt', 'r') as tum_baglantilar:
                try:
                    self.baglantilar = json.load(tum_baglantilar)
                except:
                    print("")
        except FileNotFoundError:
            print(color.UNDERLINE + color.RED + "Online user list is not created yet. First Launch Service Listener!\n" + color.END)
            time.sleep(5)
            exit()


    def listen_to_given_socket(self, musteri, adresi):
            try:
                gelen = str(musteri.recv(1024),'utf-8')
                if gelen=="EXIT":
                    print(color.BOLD+color.PURPLE+self.baglantilar_ters[adresi[0]]+" leaved the chat\n"+color.END)
                    musteri.close()
                    #break
                else:
                    time_sent = datetime.datetime.fromtimestamp(self.time_started).strftime('%Y-%m-%d %H:%M:%S')
                    log=time_sent+"   "+self.baglantilar_ters[adresi[0]]+" : "+gelen
                    print(color.BOLD+log+color.END)
                    with open('Chat_log.txt', 'a') as clog:
                        clog.write(log+"\n")
                    #break
            except UnicodeEncodeError:
                print(color.BOLD+color.PURPLE+"UnicodeEncodeError"+color.END)

if __name__ == '__main__':
    c = Listener()


