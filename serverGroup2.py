import socket
import time

HOST = '127.1.0.4'  # Standard loopback interface address (localhost)
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

import os
from _thread import *

ServerSocket = socket.socket()
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
host = '127.0.0.1'
port = 1232
ThreadCount = 0
server.bind(("", 44443))
message = b"offer 2"
while True:
    server.sendto(message, ('<broadcast>', 37020))
    print("message sent!")
    time.sleep(1)
try:
    ServerSocket.bind((host, port))
    #server.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    #connection.send(str.encode('Welcome to the Server\n'))
    message = b"offer 2"
    while True:
        connection.sendto(message, ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)
        #data = connection.recv(2048)
        #reply = 'Server Says: ' + data.decode('utf-8')
        """if not data:
            break
        connection.sendall(str.encode(reply))"""
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()