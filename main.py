import socket
import time

HOST = '172.1.0.4'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

HOST = '172.1.0.88'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

#Mysty server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
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
    time.sleep(1)

#second server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
print("Server started, listening on IP address 172.1.04")
server.bind(("", 44445))
message = b"your very important message"
while True:
    server.sendto(message, ('<broadcast>', 37020))
    print("message sent!")
    time.sleep(1)

