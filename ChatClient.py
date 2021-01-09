import socket
import threading
import json
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


PORT = 5001

all_processes = []



class Client:
    baglantilar = []
    baglantilar_ters = []
    chat_log = []
    all_processes_exit = False
    again = False

    def __init__(self):

        paralel_islem = threading.Thread(target=self.panel, args=())
        paralel_islem.daemon = True
        paralel_islem.start()
        all_processes.append(paralel_islem)

        while not self.all_processes_exit:
            time.sleep(1)
            self.update_users()

        print(color.BOLD + color.BLUE + "Ending All Processes" + color.END)
        print(color.BOLD + color.BLUE + "BYE :* \n" + color.END)
        for process in all_processes:
            process.join()
        exit()

    def panel(self):
        print(color.BOLD + color.BLUE + "1. List online users\n"
                                        "2. Connect to user\n"
                                        "3. Display Chat log\n"
                                        "4. Clear chat history\n"
                                        "5. Exit\n" + color.END)
        print(color.BOLD + color.RED + "Pelease Select the Action | Type [number] and Press ENTER" + color.END + "\n")
        cevap = input()
        if cevap == '1':
            self.display_users(1)
        elif cevap == '2':
            self.connect_user()
        elif cevap == '3':
            self.display_chat_log()
        elif cevap == '4':
            self.clear_chat_log()
        elif cevap == '5':
            self.exit()
        else:
            print(color.UNDERLINE + color.RED + "Please type a number that shown in the list" + color.END + "\n")
            self.panel()

    def clear_chat_log(self):
        with open('Chat_log.txt', 'w') as log:
            try:
                log.flush()
                print(color.BOLD + color.PURPLE + "Chat log is cleaned successfully.\n")
            except:
                time.sleep(0.01)
                print(color.BOLD + color.RED + "Try Again\n")
        self.panel()

    def display_chat_log(self):
        with open('Chat_log.txt', 'r') as log:
            try:
                self.chat_log = log.read()
            except:
                time.sleep(0.01)
        print(color.BOLD + color.PURPLE + "-------------------------------------\n")
        print(self.chat_log)
        print("-------------------------------------\n" + color.END)
        self.panel()

    def exit(self):
        self.all_processes_exit = True

    def connect_user(self):  # initiatig TCP Session
        number = self.display_users(0)
        if number == 0:
            self.panel()
        else:
            print(color.BOLD + color.RED + "Select the user [username] and press ENTER\n" + color.END)
            username = input()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.baglantilar[username]
                sock.connect((self.baglantilar[username], PORT))
                self.send_to_given_sock(sock)
            except KeyError:
                print(color.UNDERLINE + color.RED + "Typo! Please write a valid [username] and press ENTER\n" + color.END)
                self.again = True
            except ConnectionRefusedError:
                print(color.UNDERLINE + color.RED + "Connection Refused Error. The user might be gone. Try again\n" + color.END)
                self.again = True
            except:
                print(color.UNDERLINE + color.RED + "A connection error occurred. Try again\n" + color.END)
                self.again = True
            if self.again:
                paralel_islem2 = threading.Thread(target=self.connect_user)
                paralel_islem2.daemon = True
                paralel_islem2.start()
                self.again = False
                all_processes.append(paralel_islem2)

    def update_users(self):
        try:
            with open('Peers_ters.txt', 'r') as tum_baglantilar:
                try:
                    self.baglantilar_ters = json.load(tum_baglantilar)
                except:
                    time.sleep(0.01)

            with open('Peers.txt', 'r') as tum_baglantilar:
                try:
                    self.baglantilar = json.load(tum_baglantilar)
                except:
                    time.sleep(0.01)
        except FileNotFoundError:
            print(color.UNDERLINE + color.RED + "Online user list is not created yet. First Launch Service Listener!\n" + color.END)
            time.sleep(5)
            self.all_processes_exit = True

    def display_users(self, mod):
        print(color.BOLD + color.GREEN + "------------ ONLINE USERS ------------\n")
        number = 0
        for key in self.baglantilar_ters:
            print("  ", self.baglantilar_ters[key], "\n")
            number += 1
        print("--------", number, "connections listed --------\n" + color.END)
        if mod == 1:
            self.panel()
        else:
            return number

    def send_to_given_sock(self, musteri):
        print(color.BOLD + color.RED + "Type [EXIT] and Press ENTER for Returning The Panel")
        while 1:
            message = input("Type your message and press ENTER\n")
            musteri.send(bytes(message, "utf-8"))
            if message == "EXIT":
                print(color.BOLD + color.BLUE + "Connection closed\n" + color.END)
                musteri.close()
                paralel_islem3 = threading.Thread(target=self.panel, args=())
                paralel_islem3.daemon = True
                paralel_islem3.start()
                all_processes.append(paralel_islem3)
                break


if __name__ == '__main__':
    c = Client()
