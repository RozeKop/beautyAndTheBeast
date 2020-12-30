import socket
import random
import keyboard
import time
from _thread import *
import msvcrt
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print("Client started, listening for offer requests...")
portUDP = 37020
client.bind(("", portUDP))
b_m = True  # change name
while b_m:
    m_pack, addr = client.recvfrom(1024)
    m = struct.unpack('IbH', m_pack)
    cookie = hex(m[0])
    type = hex(m[1])
    port_to_connect = m[2]
    if cookie == hex(0xfeedbeef) and type == hex(0x2):
        b_m = False
print("Recived offer from ", addr[0], " attempting to connect...")
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

while True:
    """
    data,addr = client.recvfrom(1024)
    print("received message: %s" % data.decode('utf-8'))

    """
    try:
        # port = data.decode('utf-8')[6:10]
        ClientSocket.connect((host, port_to_connect))
        print("The port I am binding is Client: ", port_to_connect)
        break
    except socket.error as e:
        print(str(e))


def keyboard_client(ClientSocket, t_end):
    while time.time() < t_end:
        if msvcrt.kbhit():
            try1 = msvcrt.getch()  # read_key(True)
            ClientSocket.send(str.encode(str(try1)))
    return


Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
Input = input('Group name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
t_end = time.time() + 20
try:
    start_new_thread(keyboard_client, (ClientSocket, t_end,))  # connect to server
except:
    print("Error: unable to start thread")
stam = 0
while time.time() < t_end:
    stam += 1
print("Client is on main")
while True:
    try:
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
        break
    except:
        continue
# Response = ClientSocket.recv(1024)
# print(Response.decode('utf-8'))

while 1:
    pass

# ClientSocket.close()