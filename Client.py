import socket                                  #socket connection
import errno                                   #error handling
import sys                                     #also error handling
import time                                    #for analysis purposes
import rsa                                     #For ENCRYPTION / DECRYPTION of text
#these 3 constants are used to recieve the message lengths
HEADER_LENGTH = 10                              
PRIVATE_KEY = 10
PUBLIC_KEY = 10

IP = "127.0.0.1"                                #the ip address of our server
PORT = 1234                                     #the port it is located at
my_username = input("Enter a Username: ")       #prompts user to enter a username

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

#after connecting to the server keep track of the time
start_time = time.perf_counter()

#Set connection to non-blocking state so that we can keep sending messages without the socket stopping us
client_socket.setblocking(False)

#Since socket can only send bytes. We need to convert out strings to bytes and 
# make sure to get the length of the string we are sending, 
# elsewise, some un needed trash will follow.
username = my_username.encode('utf-8')                                  #encode to UTF-8 (unicode) as bytes
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')   #gets the length of the bytes
client_socket.send(username_header + username)                          #use the socket object to send to the server


#PRIV KEY HANDOUT
#after connecting to the server, a private session key is given out to the clients connected
#this is for decrypting the messages
client_socket.setblocking(True)                                         #we must block the client so that it can recieve things one at a time. Elsewise it will cause a failure
KEY_HEADER = client_socket.recv(PRIVATE_KEY)                              #recieve the length of the key, as explained before if we do not recieve exactly the length of the string it will cause issues
KEY_LENGTH = int(KEY_HEADER.decode('utf-8').strip())                      #gets the length of the string by decoding the unicode, removing white spaces, and converting into an integer
KEY = client_socket.recv(KEY_LENGTH).decode('utf-8')                     #finally we recieve exactly our message length and decode back into a string
KEY = int(KEY)                                                          #convert the given string back to an integer

#PUBLIC KEY HANDOUT
KEY_HEADER = client_socket.recv(PUBLIC_KEY)
KEY_LENGTH = int(KEY_HEADER.decode('utf-8').strip())
PUBKEY = client_socket.recv(KEY_LENGTH).decode('utf-8')
PUBKEY = int(PUBKEY)


#N HANDOUT
#this is needed for decryption and encryption
N_HEAD = client_socket.recv(HEADER_LENGTH)
N_LENGTH = int(N_HEAD.decode('utf-8').strip())
N = client_socket.recv(N_LENGTH).decode('utf-8')
N = int(N)

client_socket.setblocking(False)                                        #after we recieve all the keys and necessary things open the socket so we can keep sending messages

#time it took for keys to be handed out
end_time = time.perf_counter()

total_time = end_time - start_time

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If not empty -> send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        #get the int representation of the message
        byte_message = int.from_bytes(message, "big")  
        #encrypt message
        encrypted_message = rsa.encrypt(byte_message, N, PUBKEY)                        #encrypted int version of message
        #since the socket can only send bytes, convert to bytes
        encrypted_message = str(encrypted_message).encode('utf-8')                      #change int version to byte
        #send encrypted message
        message_header = f"{len(encrypted_message):<{HEADER_LENGTH}}".encode('utf-8')   #the length of the encrpted message, this will be important later for the conversion of our decrypted message
        client_socket.send(message_header + encrypted_message)


    try:
        # Loop through messages sent through the server and print them
        while True:

            # Receive username length
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data server gracefully closed a connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            message = int(message)                                                  #changed to int
            
            #now we decrypt the message
            message = rsa.decrypt(message, N, KEY)
            message_length = len(str(message))                                      #like mentioned before, the length of the decrypted message is necessary for the conversion of the integer back into a string
            message = message.to_bytes(message_length, "big")                       #converts the integer back into bytes given the meesage length sent
            message = message.decode('utf-8')                                       #decodes the bytes back into a string
            
            # Print message
            print(f'{username} > {message}')                                    

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        #something else happened send a reading error and leave the client
        print('Reading error: '.format(str(e)))
        sys.exit()
