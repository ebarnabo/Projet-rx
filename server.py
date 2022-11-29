import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#print(socket.gethostname)
s.bind((socket.gethostname(),1934))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes("Welcome","utf-8"))
    msg = clientsocket.recv(1024)