import socket
import time
import os
from _thread import *
import random
import struct
import threading
from scapy.arch import get_if_addr

ServerSocket = 0
#host = '127.0.0.12'
host = get_if_addr("eth1")
port = 1233
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
    data = connection.recv(1024)
    name = data.decode('utf-8')
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
    t_end = time.time() + 10 #change to 10
    connection.settimeout(1)
    while time.time() < t_end:
        try:
            Response = connection.recv(1024).decode('utf-8')
        except:
            continue
        if (Response):
            if connection.getpeername()[1] in portToGroup.keys():
                if portToGroup[connection.getpeername()[1]] == 1:
                    lock.acquire()
                    counter1 += max(len(Response)//4,1)
                    lock.release()
                    print("1: ", counter1)
                else:
                    lock.acquire()
                    counter2 += max(len(Response)//4,1)
                    lock.release()
                    print("2: ", counter2)
    massage = "Game over!\nGroup1 typed in " +str(counter1)+ " charecters. Group 2 typed in " +str(counter2)+ " charecters.\n"
    if counter1 > counter2:
        massage += "Group 1 wins!\n\n"
    else:
        massage += "Group 2 wins!\n\n"
    massage += "Congratulations to the winners:\n"
    massage += "==\n"
    if counter1 > counter2:
        for i in range(len(group1)):
            massage += group1[i] + "\n"
    else:
        for i in range(len(group2)):
            massage += group2[i] + "\n"
    connection.send(massage.encode())



def broadcast(ThreadCount,t_end):
    global port
    global host
    #host = "172.0.1.12"
    host = get_if_addr("eth1")
    print("Server started,listening on IP address ", host)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", 44444))
    message = struct.pack('Ibh', int(0xfeedbeef), int(0x2), port)
    while time.time() < t_end:
        server.sendto(message, ('<broadcast>', 13117))
        print("message sent!")
        time.sleep(1)


def tcpConnect(ThreadCount,t_end):
    global ServerSocket
    try:
        ServerSocket.bind((host, port+ThreadCount))
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
        t_end = time.time() + 10
        start_new_thread(broadcast, (ThreadCount,t_end)) #send brodcast
        start_new_thread(tcpConnect, (ThreadCount, t_end,)) #connect to server
    except:
       print("Error: unable to start thread")
    fin = time.time() + 25 # change time
    while time.time() < fin:
        time.sleep(1)
    for client in clients.keys():
        clients[client].close()
    ServerSocket.close()
    return True


    while 1:
        pass


def startS(num):
    main()
    #print("srvet")
    #while True:
    #    flag = False
    #    flag = main()
    #    if flag :
    #        flag = False
    #       flag = main()
