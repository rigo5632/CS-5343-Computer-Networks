#! /usr/bin/python3

import socket
import sys
import _thread
import time
import string
import packet
import udt
import random
from timer import Timer


# Some already defined parameters
PACKET_SIZE = 512
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 9090)
SLEEP_INTERVAL = 0.05 # (In seconds)
#SLEEP_INTERVAL = 10 # (In seconds)
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4
SELECTIVE_RECEIVE_STATUS = {}

# You can use some shared resources over the two threads
base = 0
mutex = _thread.allocate_lock()
timer = Timer(TIMEOUT_INTERVAL)

# Need to have two threads: one for sending and another for receiving ACKs

# Generate random payload of any length
def generate_payload(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str


# Send using Stop_n_wait protocol
def send_snw(sock):
    global base
    global timer
    global mutex

    # read file and store packets
    packets = []
    sequence = 0
    try: 
        file = open('./files/Bio.txt', 'r', encoding='utf-8')
        data = file.read(PACKET_SIZE)
    except:
        print('File does not exists')
        sys.exit(1)
    # get all data from file
    while data:
        packets.append(packet.make(sequence, data.encode()))
        data = file.read(PACKET_SIZE)
        sequence += 1
    
    #receiver thread
    _thread.start_new_thread(receive_snw, (sock, packets))

    while base < len(packets):
        currentBase = base
        print('Sending Sequence: %i' %base)
        udt.send(packets[base], sock, RECEIVER_ADDR) # send packet
        if not timer.running(): timer.start() # start timer
        
        while not timer.timeout(): # while we have time to receive packets
            if currentBase != base: break
            pass
    
        if timer.timeout(): # timeout ouccrs
            print('*** ERROR: TIMEOUT OCCUREED ***')
            base = currentBase
            timer.stop()
        time.sleep(TIMEOUT_INTERVAL)
    sys.exit(0)

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
    global base
    global timer
    global mutex


    while base < len(pkt):
        # get out packet and server packet
        currentSequence, _ = packet.extract(pkt[base])
        try:
            acknowledgement, _ = udt.recv(sock)
        except:
            print('*** ERROR: LOST CONNECTION TO SERVER')
            sys.exit(1)
        acknowledgement = int(acknowledgement.decode())
        currentSequence = int(currentSequence)

        # see if we got the correct ack
        if acknowledgement == currentSequence:
            mutex.acquire()
            base += 1
            timer.stop()
            mutex.release()
        else:
            print('\n*** ERROR: Received Incorrect Acknowledgement ***\n')
            print('Expected Acknowledgement: %i' %currentSequence) 
            print('Received Acknowledgement: %i' %acknowledgement) 
    sys.exit(0)

# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)

    send_snw(sock)
    #send_gbn(sock)
    #send_sr(sock)




