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
    global timer
    try:
        fileSource = './files/Bio.txt'
        file = open(fileSource, 'r', encoding='utf-8')
        data = file.read(PACKET_SIZE)
    except:
        print('File %s not found' %fileSource)
        sys.exit(1)
    packets = []
    seq = 0
    while data:
        packets.append(packet.make(seq, data.encode()))
        seq += 1
        data = file.read(PACKET_SIZE)
    endConnectionPacket = packet.make(seq, "END".encode())
    packets.append(endConnectionPacket)

    sock.settimeout(TIMEOUT_INTERVAL)
    while base < len(packets):
        mutex.acquire()
        sending = base
        print('Sending Sequence #: %i' %base)
        
        udt.send(packets[base], sock, RECEIVER_ADDR)
        _thread.start_new_thread(receive_snw, (sock, packets[base]))

        mutex.release()
        time.sleep(SLEEP_INTERVAL)

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
    global base
    global mutex
    global timer

    mutex.acquire()
    try:

        serverPayload, _ = udt.recv(sock)
        serverAcknowledgement = int(serverPayload.decode())
        clientSequence, _ = packet.extract(pkt)

        if serverAcknowledgement == clientSequence:
            print('Success... Updating new base')
            base += 1
    except:
        print('Client did not get server acknowldgement')


    mutex.release()

# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)


    _thread.start_new_thread(send_snw, (sock, ))

    print('Ctrl-c to quit')
    while True:
        pass


