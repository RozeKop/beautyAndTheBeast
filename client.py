import socket
import random
import keyboard
import time
from _thread import *
import msvcrt
import struct

MSG_LEN = 1024
FORMAT = 'utf-8'
SSH_HOST = ""
SSH_PORT = 2116
portUDP = 37020

def keyboard_client(ClientSocket, t_end):#start of game state

    while time.time() < t_end: #for the duration of the game given

        if msvcrt.kbhit():#if key press detected, register it and send it to the server
            try1 = msvcrt.getch()  # read_key(True)
            ClientSocket.send(str.encode(str(try1)))
    Response = ClientSocket.recv(MSG_LEN).decode(FORMAT) #end of game messege

    print(Response)




# ClientSocket.close()
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Client started, listening for offer requests...")

    client.bind(("", portUDP))#listening on broadcast
    b_m = True  # change name
    while b_m:#recieveing conenction offer
        m_pack, addr = client.recvfrom(MSG_LEN)
        m = struct.unpack('IbH', m_pack)#identifying the recieved messege as the "expected" messege by its specific format
        cookie = hex(m[0])
        type = hex(m[1])
        port_to_connect = m[2]
        if cookie == hex(0xfeedbeef) and type == hex(0x2):
            b_m = False
    print("Recived offer from ", addr[0], " attempting to connect...")
    ClientSocket = socket.socket()
    host = SSH_HOST

    while True:
        try:
            ClientSocket.connect((host, SSH_PORT))#attempting to connect to TCP server

            break
        except socket.error as e:
            print(str(e))
    Response = ClientSocket.recv(MSG_LEN )#welcome messege for group registration
    print(Response.decode(FORMAT))
    Input = input('Group name: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(MSG_LEN) #recieving and printing game instructions from server
    print(Response.decode(FORMAT))
    t_end = time.time() + 20
    keyboard_client(ClientSocket, t_end)#starting game
    stam = 0
    while time.time() < t_end:
        stam += 1
    print("Client is on main")
    while True:
        try:
            print("Server disconnected, listening for offer request...")
            ClientSocket.close()
            return True
            break
        except:
            continue


    while 1:
        pass


while True:#runs until manually interrupted
    flag = False
    flag = main()
    if flag :
        flag = False
        flag = main()