import socket
import time
import os
from _thread import *
import random



HOST = '172.1.0.4'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(), PORT)) #change to HOST later
    s.listen()
    print("Server started, listening on IP address 172.1.04")
    conn, addr = s.accept()
    with conn:
        #print("Server started, listening on IP address 172.1.04")
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
"""

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
"""server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
print("Server started, listening on IP address 172.1.04")
server.bind(("", 44444))
message = b"your very important message"
while True:
    server.sendto(message, ('<broadcast>', 37020))
    print("message sent!")
    time.sleep(1)"""

ServerSocket = socket.socket()

group1 = []
group2 = []
def threaded_client(connection):
    connection.sendall(str.encode("please write your team name"))
    data = connection.recv(1024)
    name = data.decode('utf-8')
    print(name)
    print(name[:len(name)-2])
    choose_group = random.randint(1, 2)
    if choose_group == 1:
        if len(group1) < 2:
            group1.append(name[:len(name)-2])
        else:
            group2.append(name[:len(name) - 2])
    else:
        if len(group2) < 2:
            group2.append(name[:len(name)-2])
        else:
            group1.append(name[:len(name) - 2])
    print(group1)
    print(group2)
    connection.close()


def broadcast():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", 44444))
    message = b"offer"
    t_end = time.time() + 20 #change to 10
    while time.time() < t_end:
        server.sendto(message, ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)


def tcpConnect():
    host = '127.0.0.1'
    port = 1233
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
        # server.bind((host, port))
    except socket.error as e:
        print(str(e))

    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()


try:
    start_new_thread(broadcast, ()) #send brodcast
    start_new_thread(tcpConnect, ()) #connect to server
except:
   print("Error: unable to start thread")


while 1:
   pass





