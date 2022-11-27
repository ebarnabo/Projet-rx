import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#print(socket.gethostname)
s.bind((socket.gethostname(),1934))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print("La connexion depuis {address} a été établie !")
    clientsocket.send(bytes("Welcome bitch","utf-8"))