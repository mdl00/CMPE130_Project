import socket
import select
import rsa
import time
#CREATE KEYS
start_time = time.perf_counter()            #this is for keeping track of runtime
p = rsa.generate_prime(1024)
q = rsa.generate_prime(1024) 
#This is rsa 2048
n = p * q

PUBLIC_KEY = rsa.get_public_key()            #predefined constant
PRIVATE_KEY = rsa.create_private_key(p,q)    #create private key given p and q

end_time = time.perf_counter()

total_time = (end_time - start_time)

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

#List of connected clients - socket as a key, user header and name as data
clients = {}

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

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('NEW CLIENT CONNECTED: {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            # HELP!!!!!!!!!!!!!!!!!!!!! Need to send key over to connected client. However, the send function returns an byte of b'' even though the privKey is b'(some value for key)'
            privKey = str(PRIVATE_KEY).encode('utf-8')
            keyHeader = f"{len(privKey):<{HEADER_LENGTH}}".encode('utf-8')

            client_socket.send(keyHeader + privKey)

            pubKey = str(PUBLIC_KEY).encode('utf-8')
            keyHeader = f"{len(pubKey):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(keyHeader + pubKey)

            modN = str(n).encode('utf-8')
            n_header = f"{len(modN):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(n_header + modN)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #note it works now.

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('{} DISCONNECTED'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

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
