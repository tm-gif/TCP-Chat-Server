import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")
the_password = input("Password: ")


# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, then we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

#Prepare password and header to be sent
#encode the password to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
password = the_password.encode('utf-8')
password_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(password_header + password)


while True:
        
    # Client and server communicate
    message = input(f'{my_username} > ')
    
    # If message is not empty
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message) #send
        
        #In charge of disconnecting the client
        if message == b'/exit':
            print('Connection closed by the server')
            client_socket.close()
            exit()

    try:
        # How the client recieves data from the server about another client
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)
            
            # If we received no data, server closed connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())
            
            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

         
            print(f'{username} > {message}')

    except IOError as e:
        # Different error
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        #nothing recieved
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()