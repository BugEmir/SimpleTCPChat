# Simpele TCP Chat server | We maken gebruik van SOCK_STREAM & AF_INET
# Gemaakt door: Emirhan Sarikaya
# voor educatieve doeleinden


import socket
import threading
import time

serverHost =  '127.0.0.1' # nu op localhost
serverPort = 9382 # ik heb 'm op 83722

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind((serverHost, serverPort))
serverSocket.listen()

clients = []
nickName = []


# functie voor message's broadcasten in gehele TCP channel
def broadMSG(message):
    for client in clients:
        client.send(message)

# client handler voor TCP chatroom
def handleClients(client):
    while True:
        try:
            message = client.recv(1024) 
            broadMSG(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            userNick = nickName[index]
            time.sleep(1)
            broadMSG(f'\033[37m {userNick} \033[0m heeft de chat verlaten..'.encode('ascii'))
            nickName.remove(userNick)
            break

# Client receiver
def receiveclientVerbinding():
    while True:
        client, address = serverSocket.accept()
        print(f"Verbonden met {str(address)}")

        client.send('NICK'.encode('ascii')) # we converten naar ASCII
        userNick = client.recv(1024).decode('ascii') # username voor Server
        nickName.append(userNick)
        clients.append(client)
        print(f'Gebruikersnaam van bezoeker is: {userNick}!')
        broadMSG(f'Welkom! {userNick}'.encode('ascii'))
        client.send('Verbonden met de server!'.encode('ascii'))

        relayThread = threading.Thread(target=handleClients, args=(client,))
        relayThread.start()

print("\033[37m [+] TCP chat v1.2.... \033[0m")
time.sleep(2)
print("\033[33m [+] TCP server aan het listenen.. \033[0m")
receiveclientVerbinding()
