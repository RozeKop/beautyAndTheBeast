import socket
import time
import os
from _thread import *
import random
import struct
import threading




ServerSocket = 0
MSG_LEN = 1024
FORMAT = 'utf-8'
SSH_HOST = ""
SSH_PORT = 2116
portUDP = 44444
sendUDP = 37020
ThreadCount = 0
group1 = []
group2 = []
portToGroup ={}
clients = {}
choose_team =0
counter1 = 0
counter2 = 0
lock = threading.Lock()

def threaded_client(connection, t_end):
    global clients
    global choose_team
    connection.sendall(str.encode("please write your team name"))
    data = connection.recv(MSG_LEN)
    name = data.decode(FORMAT)
    choose_group = random.randint(1, 2)
    if choose_team == 0:
        group1.append(name[:len(name)-1])
        portToGroup[connection.getpeername()[1]] = 1
        choose_team = 1
    else:
        group2.append(name[:len(name)-1])
        portToGroup[connection.getpeername()[1]] = 2
        choose_team = 0
    print(group1)
    print(group2)
    stam = 0
    while time.time() < t_end:
        stam += 1

    start_new_thread(welcome_message,(connection,))



def welcome_message(connection):
    global counter1
    global counter2
    massage = "Welcome to Keyboard Spamming Battle Royal\nGroup1:\n"
    massage += "==\n"
    for i in range(len(group1)):
        massage += group1[i] + "\n"
    massage += "Group2:\n==\n"
    for i in range(len(group2)):
        massage += group2[i] + "\n"
    massage += "\n\n"
    massage += "start pressing keys on your keyboard as fast as you can!!\n"
    connection.send(massage.encode())
    t_end = time.time() + 10
    connection.settimeout(1)
    while time.time() < t_end:
        try:
            Response = connection.recv(MSG_LEN).decode(FORMAT)
        except:
            continue

        if (Response):
            if connection.getpeername()[1] in portToGroup.keys():
                # print(connection.getpeername()[1])
                if portToGroup[connection.getpeername()[1]] == 1:
                    lock.acquire()
                    counter1 += max(len(Response)//4,1)
                    lock.release()
                    print("1: ", counter1)
                else:
                    lock.acquire()
                    counter2 += max(len(Response) // 4, 1)
                    lock.release()
                    print("2: ", counter2)

    massage = "Game over!\nGroup1 typed in " +str(counter1)+ " characters. Group 2 typed in " +str(counter2)+ " charecters.\n"
    if counter1 > counter2:
        massage += "Group 1 wins!"+"\n\n"
    else:
        massage += "Group 2 wins!"+"\n\n"
    massage += "Congratulations to the winners:\n"
    massage += "==\n"
    if counter1 > counter2:
        for i in range(len(group1)):
            massage += group1[i] + "\n"
    else:
        for i in range(len(group2)):
            massage += group2[i] + "\n"
    connection.send(massage.encode())





def broadcast(ThreadCount):
    print("Server started,listening on IP address ", SSH_HOST)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind((SSH_HOST, portUDP))
    #message = "offer " + str(port + ThreadCount)
    message = struct.pack('IbH', 0xfeedbeef, 0x2, SSH_PORT)
    t_end = time.time() + 10 #change to 10
    while time.time() < t_end:
        server.sendto(message, ('<broadcast>', sendUDP))
        print("message sent!")
        time.sleep(1)


def tcpConnect(ThreadCount,t_end):
    global ServerSocket
    try:
        ServerSocket.bind((SSH_HOST, SSH_PORT+ThreadCount))
        print("The port I am binding is: ", SSH_PORT+ThreadCount)
        # server.bind((host, port))
    except socket.error as e:
        print(str(e))

    ServerSocket.listen(5)

    while True:
        try:
            Client, address = ServerSocket.accept()
        except:
            continue
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        clients[address[1]] = Client
        start_new_thread(threaded_client, (Client,t_end,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))





def main():
    global ServerSocket
    global clients
    global counter2
    global counter1
    global group1
    global group2
    global portToGroup
    counter2 = 0
    counter1 = 0
    clients ={}
    portToGroup = {}
    group1 = []
    group2 = []
    try:
        ServerSocket = socket.socket()
        start_new_thread(broadcast, (ThreadCount,)) #send brodcast
        t_end = time.time() + 20  # change to 10
        start_new_thread(tcpConnect, (ThreadCount, t_end,)) #connect to server
    except:
       print("Error: unable to start thread")
    fin = time.time() + 40
    while time.time() < fin:
        time.sleep(1)
    for client in clients.keys():
        clients[client].close()
    ServerSocket.close()
    return True


    while 1:
        pass


while True:
    flag = False
    flag = main()
    if flag:
        flag = False
        flag = main()

