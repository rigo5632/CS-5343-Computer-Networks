#! /usr/bin/python3

from scapy.all import *
import re

def print_pkt(pkt):
	pkt.show()

def print_icmp_pkts():
	pkt = sniff(filter='icmp', prn=print_pkt)

def print_all_pkts():
	pkt = sniff(prn=print_pkt)

def print_specific_pkts():
	ip_info = str(input('Look for ip:port: '))
	ip_info = re.split(':', ip_info)
	pkt_filter = (('tcp and host %s and port %s') %(ip_info[0], ip_info[1]))
	pkt = sniff(filter=pkt_filter, prn=print_pkt)


print('1. print all packets')
print('2. print icmp packets')
print('3. print tcp with destination <ip>:<port>')

option = int(input('$ '))

if option == 1:
	print_all_pkts()
elif option == 2:
	print_icmp_pkts()
elif option == 3:
	print_specific_pkts()
else:
	print('Invalid option')
