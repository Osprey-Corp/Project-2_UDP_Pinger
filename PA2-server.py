# Server.py
# We will need the following module to generate
# randomized lost packets
import random
from socket import *

# Ping number counter
pingnum = 0

# Create a UDP socket, notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('10.0.0.1', 12000))

print('Waiting for Client...\n')

while True:

    # Count the pings received
    pingnum += 1

    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the
    # address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Message is decoded from byte array to string.
    message_rcvd = message.decode()

    # Message is capitalize. 
    message_sent = message.decode().upper()

    # If rand is less is than 4, and this not the
    # first "ping" of a group of 10, consider the
    # packet lost and do not respond
    if rand < 4 and pingnum % 10 != 1:
        print('Packet ' + str(pingnum) + ' was lost.\n')
        continue

    # Otherwise, the server responds
    serverSocket.sendto(message_sent.encode(), address)

    # Message received and sent along with ping number are displayed.
    print('PING ' + str(pingnum) + ' Received')
    print('Mesg rcvd: ' + message_rcvd)
    print('Mesg sent: ' + message_sent + '\n')
