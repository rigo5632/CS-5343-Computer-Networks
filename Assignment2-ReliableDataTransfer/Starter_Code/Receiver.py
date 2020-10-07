#! /usr/bin/python3
# receiver.py - The receiver in the reliable data transer protocol
import packet
import socket
import sys
import udt
from timer import Timer

RECEIVER_ADDR = ('localhost', 8080)

# Receive packets from the sender w/ GBN protocol
def receive_gbn(sock):
    # Fill here
    sock.settimeout(10)
    while True:
        try:
            clientPacket, clientAddress = udt.recv(sock)
        except:
            print('Server Shutting Down')
            sys.exit(1)
        
        clientSequence, clientData = packet.extract(clientPacket)
        print(clientSequence)
        acknowledgement = packet.make(clientSequence, str(clientSequence).encode())
        udt.send(acknowledgement, sock, clientAddress)
    return


# Receive packets from the sender w/ SR protocol
def receive_sr(sock, windowsize):
    # Fill here
    sock.settimeout(10)
    while True:
        try:
            clientPacket, clientAddress = udt.recv(sock)
        except:
            print('Server Shutting Down')
            sys.exit(1)
        
        clientSequence, clientData = packet.extract(clientPacket)
        print(clientSequence)
        acknowledgement = packet.make(clientSequence, str(clientSequence).encode())
        udt.send(acknowledgement, sock, clientAddress)
    return

# Receive packets from the sender w/ Stop-n-wait protocol
def receive_snw(sock):
    try: # open file
        file = open('./files/receiver_bio.txt', 'a')
    except: # cannot create file
        print('Could Access location')
        sys.exit(1)
    sock.settimeout(10) # socket timer
    data = ''
    previous = -1
    while data != 'END': 
        try: clientPacket, senderAddress = udt.recv(sock) # client response
        except: break
        clientSequence, clientPayload = packet.extract(clientPacket)
        data = clientPacket.decode()
        print('Seq#: %i' % clientSequence)
        if previous != clientSequence: file.write(clientPayload.decode()) # write data to file
        acknowledgement = str(clientSequence).encode() # generate ack and send
        udt.send(acknowledgement, sock, senderAddress)
        previous = clientSequence # update last seen client sequence

# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    #receive_snw(sock)
    #receive_gbn(sock)
    receive_sr(sock, 7//2)
    # Close the socket
    sock.close()