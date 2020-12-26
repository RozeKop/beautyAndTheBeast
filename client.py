import socket

"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((socket.gethostname(),65432))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))"""

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print("Client started, listening for offer requests...")
client.bind(("", 37020))
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
    print("received message: %s" % data)
    print("Recived offer from " , addr[0] , " attempting to connect...")
    try:
        ClientSocket.connect((host, port))
        break
    except socket.error as e:
        print(str(e))


Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
Input = input('Group name: ')
ClientSocket.send(str.encode(Input))
    #Response = ClientSocket.recv(1024)
    #print(Response.decode('utf-8'))

ClientSocket.close()