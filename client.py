import socket
import random
import time
from _thread import *
import getch
import struct
import sys, errno
from signal import signal, SIGPIPE, SIG_DFL
from scapy.arch import get_if_addr


def keyboard_client(ClientSocket, t_end):
    while time.time() < t_end:
        #if getch.kbhit():
        try:
            try1 = getch.getch()
            ClientSocket.send(str.encode(str(try1)))
        except IOError as e:
            if e.errno == errno.EPIPE:
            #signal(SIGPIPE,SIG_DFL)
                print("error")
                break
    return

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Client started, listening for offer requests...")
    portUDP = 13117
    client.bind(("", portUDP))
    flag = True  # change name
    while flag:
        m_pack, addr = client.recvfrom(1024)
        m = struct.unpack('Ibh', m_pack)
        cookie = hex(m[0])
        type = hex(m[1])
        port_to_connect = m[2]
        print(port_to_connect)
        if cookie == hex(0xfeedbeef) and type == hex(0x2):
            flag = False
    print("Recived offer from ", addr[0], " attempting to connect...")
    ClientSocket = socket.socket()
    #host = '127.0.0.12'
    host = get_if_addr("eth1")
    port = 1233

    while True:
        try:
            ClientSocket.connect((host, port_to_connect))

            break
        except socket.error as e:
            print(str(e))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    Input = input('Group name: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    t_end = time.time() + 10
    keyboard_client(ClientSocket, t_end)
    stam = 0
    while time.time() < t_end:
        stam += 1
    while True:
        try:
            Response = ClientSocket.recv(1024).decode('utf-8')
            print(Response)
            print("Server disconnected, listening for offer request...")
            ClientSocket.close()
            return True
            break
        except:
            continue

    while 1:
        pass

def start(num):
    main()
    #print("client")
    #while True:
    #    flag = False
    #    flag = main()
    #    if flag :
    #        flag = False
    #        flag = main()

