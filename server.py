import socket
import time
import os
from _thread import *
import random
import struct
import threading
#from scapy.arch import get_if_addr # for ssh

ServerSocket = 0
MSG_LEN = 1024
FORMAT = 'utf-8'
SSH_HOST = '127.0.0.1' # get_if_addr("eth1") - for ssh
SSH_PORT = 2116
portUDP = 44444
sendUDP = 13117
ThreadCount = 0
group1 = []
group2 = []
portToGroup = {}
clients = {}
choose_team = 0
counter1 = 0
counter2 = 0
lock = threading.Lock()


"""
this function is in charge of splitting the the clients into groups and staring the game
"""
def threaded_client(connection, t_end):
    global clients
    global choose_team
    connection.sendall(str.encode("please write your team name"))
    data = connection.recv(MSG_LEN)  # recieves team name from client
    name = data.decode(FORMAT)

    #######splits incoming client between both groups equally
    if choose_team == 0:
        group1.append(name[:len(name) - 1])
        portToGroup[connection.getpeername()[1]] = 1
        choose_team = 1
    else:
        group2.append(name[:len(name) - 1])
        portToGroup[connection.getpeername()[1]] = 2
        choose_team = 0
    stam = 0
    while time.time() < t_end:
        stam += 1

    start_new_thread(welcome_message, (connection,))  # initiate game state


def welcome_message(connection):
    # global counters that count each groups point total
    global counter1
    global counter2

    # writes welcome message for both teams and sends to all the clients
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
    connection.settimeout(1)  # if no input is received, prevents locking
    while time.time() < t_end:
        try:
            Response = connection.recv(MSG_LEN).decode(FORMAT)  # receiving key press from client
        except:
            continue

        if (Response):
            # adds the points for key presses to the relevant team
            # (locks the relevant counter so threads don't overlap each other's value)
            # the server also prints server side in real time how many keys each group pressed so far
            if connection.getpeername()[1] in portToGroup.keys():
                if portToGroup[connection.getpeername()[1]] == 1:
                    lock.acquire()
                    counter1 += max(len(Response) // 4, 1)
                    lock.release()
                else:
                    lock.acquire()
                    counter2 += max(len(Response) // 4, 1)
                    lock.release()

    # creates end of game message, announces the winning team and sends to all the clients
    massage = "Game over!\nGroup1 typed in " + str(counter1) + " characters. Group 2 typed in " + str(
        counter2) + " charecters.\n"
    if counter1 > counter2:
        massage += "Group 1 wins!" + "\n\n"
    else:
        massage += "Group 2 wins!" + "\n\n"
    massage += "Congratulations to the winners:\n"
    massage += "==\n"
    if counter1 > counter2:
        for i in range(len(group1)):
            massage += group1[i] + "\n"
    else:
        for i in range(len(group2)):
            massage += group2[i] + "\n"
    connection.send(massage.encode()) #sending the end Game message

"""
this function opens the UDP socket and sends the 
"""
def broadcast(ThreadCount):
    global SSH_HOST
    global SSH_PORT
    print("Server started,listening on IP address ", SSH_HOST)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", portUDP))  # broadcasting UDP offer
    message = struct.pack('IbH', hex(0xfeedbeef), hex(0x2),SSH_PORT)  # sending valid broadcast message to indentify ourselves as the "correct" server
    t_end = time.time() + 10
    while time.time() < t_end:
        server.sendto(message, ('<broadcast>', sendUDP))
        time.sleep(1)

"""
connecting the clients via TCP
"""
def tcpConnect(ThreadCount, t_end):
    global SSH_HOST
    global SSH_PORT
    global ServerSocket
    try:
        ServerSocket.bind((SSH_HOST, SSH_PORT))  # opening socket for incoming client
    except socket.error as e:
        print(str(e))

    ServerSocket.listen(5)  # listening on incoming client

    while True:
        try:
            Client, address = ServerSocket.accept()  # connecting client to server
        except:
            continue
        clients[address[1]] = Client  # saving all our connections for later use
        start_new_thread(threaded_client, (Client, t_end,))  # starting new thread for game state
        ThreadCount += 1


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
    clients = {}
    portToGroup = {}
    group1 = []
    group2 = []
    try:
        ServerSocket = socket.socket()
        start_new_thread(broadcast, (ThreadCount,))  # send brodcast
        t_end = time.time() + 10
        start_new_thread(tcpConnect, (ThreadCount, t_end,))  # connect to tcp server
    except:
        print("Error: unable to start thread")
    fin = time.time() + 25
    while time.time() < fin:
        time.sleep(1)
    for client in clients.keys():  # at the end of the run close all connections
        clients[client].close()
    ServerSocket.close()  # at the end of run close server socket
    return True

    while 1:
        pass


while True:  # runs until manually interrupted
    flag = False
    flag = main()
    if flag:
        flag = False
        flag = main()
