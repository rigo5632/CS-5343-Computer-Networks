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
#SLEEP_INTERVAL = 0.05 # (In seconds)
SLEEP_INTERVAL = 1 # (In seconds)
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4

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
    global mutex
    try: # check if file exists and if it does get the first packet
        fileSource = './files/Bio.txt'
        file = open(fileSource, 'r', encoding='utf-8')
        data = file.read(PACKET_SIZE)
    except: # file does not exists
        print('File %s not found' %fileSource)
        sys.exit(1)
    packets = []
    seq = 0
    while data: # stores all payloads 
        packets.append(packet.make(seq, data.encode()))
        seq += 1
        data = file.read(PACKET_SIZE) # gets all new packet from file
    endConnectionPacket = packet.make(seq, "END".encode()) # adds packet to end connection
    packets.append(endConnectionPacket)

    sock.settimeout(TIMEOUT_INTERVAL) # timeout to send new packages
    while base < len(packets):
        if base == len(packets): break
        mutex.acquire() # share resources
        print('Sending Sequence #: %i' %base)
        
        udt.send(packets[base], sock, RECEIVER_ADDR) # send packet
        _thread.start_new_thread(receive_snw, (sock, packets)) # new thread: receieve messages

        mutex.release() # release lock
        time.sleep(SLEEP_INTERVAL) # cooldown
    sys.exit(0) # close Thread 1

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
    global base
    global mutex
    global timer

    if base == len(pkt): return
    mutex.acquire() # share resources
    try:
        serverPayload, _ = udt.recv(sock) # wait for server response
        serverAcknowledgement = int(serverPayload.decode()) 
        clientSequence, _ = packet.extract(pkt[base])

        if serverAcknowledgement == clientSequence: # Check if the acknowledgement is correct
            print('Success... Updating new base')
            base += 1 # update base, new packet will be sent
    except: # Client did not get response from server, either through timeout or lost package
        print('Client did not get server acknowldgement')
    mutex.release()
    sys.exit(0) # Close Thread 2

# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)

    _thread.start_new_thread(send_snw, (sock, ))

    print('Ctrl-c to quit')
    while True:
        if base == 8: break # break 
        pass


