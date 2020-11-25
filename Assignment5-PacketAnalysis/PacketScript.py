#! /usr/bin/python3

import numpy as np
import scipy
from matplotlib import pyplot as plt

def getAveragePacketSize(packets):
    packetSizes = 0
    for packet in packets: packetSizes += packets[packet]['packetBytes']
    return packetSizes // len(packets)

def getFlowDurations(packets):
    flowDurations = []
    for packet in packets: flowDurations.append(packets[packet]['timestampEnd'] - packets[packet]['timestampStart'])
    return flowDurations

def getFlowSizes(packets):
    packetData = []
    for packet in packets: packetData.append([packets[packet]['numberOfPackets'], packets[packet]['packetBytes']])
    return packetData


def displayAllData(average):
    print(f'Average Packet Sizes: {average}')

packetData = np.genfromtxt('./Packet-Data/Netflow_dataset.csv', delimiter=',')

packetID = 0
packets = {}

for data in packetData:
    packets[str(packetID)] = {
        'numberOfPackets':          data[4],
        'packetBytes':              data[5],
        'timestampStart':           data[6],
        'timestampEnd':             data[7],
        'sourceAddress':            data[10],
        'destinationAddress':       data[11],
        'sourcePort':               data[15],
        'destinationPort':          data[16],
        'protocol':                 data[17],
        'sourceNetmask':            data[20],
        'destinationNetmask':       data[21],
        'sourceAutonomous':         data[22],
        'destinationAutonomous':    data[23]
    }
    packetID += 1

average = getAveragePacketSize(packets)

displayAllData(average)
