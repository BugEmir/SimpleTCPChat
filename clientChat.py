# Simpele TCP Chat client | We maken gebruik van SOCK_STREAM & AF_INET
# Gemaakt door: Emirhan Sarikaya
# voor educatieve doeleinden



import socket
import threading
import time

nickName = input("\033[34m Kies een gebruikersnaam:  \033[0m ")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 9382))

def receiveMessages():
    while True:
        try:
            message = clientSocket.recv(1024).decode('ascii')
            if message == 'NICK':
                clientSocket.send(nickName.encode('ascii'))
            else:
                print(message)
        except:
            print("Er is een probleempie!")
            clientSocket.close()
            break

def writeMsg():
    while True:
        message = f'\033[37m {nickName} \033[0m: \033[35m {input("")} \033[0m'
        clientSocket.send(message.encode('ascii'))


ontvangThread = threading.Thread(target=receiveMessages)
ontvangThread.start()
verstuurThread = threading.Thread(target=writeMsg)
verstuurThread.start()

