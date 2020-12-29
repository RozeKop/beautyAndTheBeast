import socket
import time
import os
from _thread import *
import random
import keyboard

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
group1 = []
group2 = []
portToGroup ={}
clients = {}


def threaded_client(connection, t_end):
    global clients
    connection.sendall(str.encode("please write your team name"))
    data = connection.recv(1024)
    name = data.decode('utf-8')
    print(name)
    print(name[:len(name)-2])
    choose_group = random.randint(1, 2)
    if choose_group == 1:
        if len(group1) < 2:
            group1.append(name[:len(name)-2])
            portToGroup[connection.getpeername()[1]] = 1
        else:
            group2.append(name[:len(name) - 2])
            portToGroup[connection.getpeername()[1]] = 2
    else:
        if len(group2) < 2:
            group2.append(name[:len(name)-2])
            portToGroup[connection.getpeername()[1]] = 2
        else:
            group1.append(name[:len(name) - 2])
            portToGroup[connection.getpeername()[1]] = 1
    print(group1)
    print(group2)
    stam = 0
    while time.time() < t_end:
        stam += 1
    for client in clients.keys():
        start_new_thread(welcome_message, (clients[client],))
    #welcome_message(connection)
    #connection.close()


def welcome_message(connection):
    print("the first connection",connection)
    counter1 = 0
    counter2 = 0
    massage = "Welcome to Keyboard Spamming Battle Royal\nGroup1:\n"
    massage += "==\n"
    massage += group1[0] + "\n"
    massage += group1[1] + "\n"
    massage += "Group2:\n==\n"
    massage += group2[0] + "\n"
    massage += group2[1] + "\n\n\n"
    massage += "start pressing keys on your keyboard as fast as you can!!\n"
    connection.sendall(massage.encode())
    while True:
        Response = connection.recv(1024)
        print(Response.decode('utf-8'))
        if (Response):
            if connection.getpeername()[1] in portToGroup.keys():
                print(connection.getpeername()[1])
                if portToGroup[connection.getpeername()[1]] == 1:
                    counter1 += len(Response)
                    print("1: ", counter1)
                else:
                    counter2 += len(Response)
                    print("2: ", counter2)


def broadcast(ThreadCount):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", 44444))
    message = "offer " + str(port + ThreadCount)
    t_end = time.time() + 30 #change to 10
    while time.time() < t_end:
        server.sendto(message.encode(), ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)


def tcpConnect(ThreadCount,t_end):
    try:
        ServerSocket.bind((host, port+ThreadCount))
        print("The port I am binding is: ", port+ThreadCount)
        # server.bind((host, port))
    except socket.error as e:
        print(str(e))

    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        clients[address[1]] = Client
        start_new_thread(threaded_client, (Client,t_end,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()


try:
    start_new_thread(broadcast, (ThreadCount,)) #send brodcast
    t_end = time.time() + 30  # change to 10
    start_new_thread(tcpConnect, (ThreadCount, t_end,)) #connect to server
except:
   print("Error: unable to start thread")


while 1:
   pass





