import socket
import time
import os
from _thread import *
import random
import struct

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
group1 = []
group2 = []
portToGroup ={}
clients = {}
choose_team =0
counter1 = 0
counter2 = 0


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
    # for client in clients.keys():
    #     try:
    #         start_new_thread(welcome_message, (clients[client],))
    #
    #
    #     except:
    #         print("Error: unable to start thread")
    start_new_thread(welcome_message,(connection,))
    #welcome_message(connection)
    #connection.close()


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
        print(t_end - time.time())
        if (Response):
            if connection.getpeername()[1] in portToGroup.keys():
                # print(connection.getpeername()[1])
                if portToGroup[connection.getpeername()[1]] == 1:
                    counter1 += len(Response)//4
                    print("1: ", counter1)
                else:
                    counter2 += len(Response)//4
                    print("2: ", counter2)
    print("heree?????????")
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
    # connection.close()




def broadcast(ThreadCount):
    global port
    global host
    print("Server started,listening on IP address ", host)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", 44444))
    #message = "offer " + str(port + ThreadCount)
    message = struct.pack('IbH', 0xfeedbeef, 0x2, port)
    t_end = time.time() + 10 #change to 10
    while time.time() < t_end:
        server.sendto(message, ('<broadcast>', 37020))
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
        # threaded_client(Client, t_end)
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()


try:
    start_new_thread(broadcast, (ThreadCount,)) #send brodcast
    t_end = time.time() + 20  # change to 10
    start_new_thread(tcpConnect, (ThreadCount, t_end,)) #connect to server
except:
   print("Error: unable to start thread")


while 1:
   pass





