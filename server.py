import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# Créer un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#le serveur informe le système d'exploitation qu'il va utiliser l'adresse IP et le port donnés
server_socket.bind((IP, PORT))

# Le serveur écoute les nouvelles connexions
server_socket.listen()

# Liste des sockets pour select.select()
sockets_list = [server_socket]

# Liste des clients connectés
clients = {}

print(f'Serveur en attente de connexion {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:

            # Accepter la nouvelle connexion
            client_socket, client_address = server_socket.accept()

            # Le client doit envoyer son nom
            user = receive_message(client_socket)

            if user is False:
                continue


            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Connexion confirmée de {}:{}, pseudo: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Déconnexion de : {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Suppression de la liste 
                sockets_list.remove(notified_socket)

                # Suppression du client dans la liste
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Nouveau message de {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]