import socket
import select
import rsa
import time
#CREATE KEYS
p = rsa.generate_prime(1024)
q = rsa.generate_prime(1024) 
#This is rsa 2048
n = p * q
PUBLIC_KEY = rsa.get_public_key()            #predefined constant
PRIVATE_KEY = rsa.create_private_key(p,q)    #create private key given p and q
#length of messages
HEADER_LENGTH = 10

IP = "127.0.0.1"                            #our server address *note this is a local address.
PORT = 1234                                 #what port our server is using

#Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket options. This allows us to reuse the same address in case some ports are filled up we can keep using the same one.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind, so server informs operating system that it's going to use given IP and port
server_socket.bind((IP, PORT))

#Look for connections to the server
server_socket.listen()

#List of sockets
sockets_list = [server_socket]

#List of clients in the server
clients = {}

#messages for the server when the server is created
print('New server created')
print('New private key created')
print(f'Listening for connections on {IP}:{PORT}...')

#If message is recieved this keeps track of it and displays it to the user
def receive_message(client_socket):

    try:

        #Recieve message length
        message_header = client_socket.recv(HEADER_LENGTH)

        #Error handling, if nothing is sent return no message receieved
        if not len(message_header):
            return False

        #Convert message length back to int value after decoding from unicode
        message_length = int(message_header.decode('utf-8').strip())

        #Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    #eception handling, if we did not recieve a message correctly
    except:
        return False

while True:

    #select.select has 3 parameters(rlist, wlist, xlist)
    #it returns 3 lists: reading list, writing list, error list
    read_sockets, temp, exception_sockets = select.select(sockets_list, [], sockets_list)   #writing list is unused thus is labeled temp


    
    #Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket it is a new connection
        if notified_socket == server_socket:

            # Accept new connection
            #returns the client socket and its address
            client_socket, client_address = server_socket.accept()

            #Recieve client name
            user = receive_message(client_socket)

            # client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('NEW CLIENT CONNECTED: {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))    #new client is connected, prompt message to server
            
            privKey = str(PRIVATE_KEY).encode('utf-8')                          #since new client is connected, we send them the keys   #prepares key in bytes to send to client
            keyHeader = f"{len(privKey):<{HEADER_LENGTH}}".encode('utf-8')      #key length

            client_socket.send(keyHeader + privKey)                             #send key length + key

            pubKey = str(PUBLIC_KEY).encode('utf-8')                            #public key preparation
            keyHeader = f"{len(pubKey):<{HEADER_LENGTH}}".encode('utf-8')       #key length
            client_socket.send(keyHeader + pubKey)                              #send key length + key

            modN = str(n).encode('utf-8')                                       #sends the mod n section, preparation
            n_header = f"{len(modN):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(n_header + modN)
            

        # Else existing socket is sending a message
        else:

            # Receive message given a length
            message = receive_message(notified_socket)

            # If False, client has disconnected from the socket
            if message is False:
                print('{} DISCONNECTED'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from client list
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                #make sure we dont send the socket to themselves
                if client_socket != notified_socket:

                    # We are reusing message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
