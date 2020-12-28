import socket
import random
import keyboard
import time

"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((socket.gethostname(),65432))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))"""
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print("Client started, listening for offer requests...")
portUDP = 37020
#portUDP = random.randint(1234, 3000)
#while True:
    #try:
client.bind(("", portUDP))
#print("hereOnceAgain")
        #break
    #except:
        #print("here")
        #portUDP +=1
"""
while True:
    data = client.recv(1024)
    print("received message: %s"%data)
    print("Recived offer from 172.1.04, attempting to connect...")"""

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233


while True:
    data,addr = client.recvfrom(1024)
    print("received message: %s" % data.decode('utf-8'))
    print("Recived offer from " , addr[0] , " attempting to connect...")
    try:
        port = data.decode('utf-8')[6:10]
        ClientSocket.connect((host, int(port)))
        print("The port I am binding is Client: ", port)
        break
    except socket.error as e:
        print(str(e))


Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
Input = input('Group name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
t_end = time.time() + 50
while time.time() < t_end:
    try1 = keyboard.read_key(True)
    ClientSocket.send(str.encode(try1))
    #Response = ClientSocket.recv(1024)
    #print(Response.decode('utf-8'))

ClientSocket.close()