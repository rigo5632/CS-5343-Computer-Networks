import numpy as np
import scipy.stats
from matplotlib import pyplot as plt
from PrintData import printAverageSize, printTopPorts, printAddressTraffic, printMaskTraffic

class PacketManager():
    def __init__(self):
        self.packetFile = np.genfromtxt('./Packet-Data/Netflow_dataset_small.csv', delimiter=',', dtype=None, encoding=None)
        self.packets = {}
        self.packetID = 1
        self.averageSize = 0
        self.totalBytes = 0
        self.flowDurations = []
        self.flowSizes = []
        self.sourcePorts = {}
        self.destinationPorts = {}
        self.sourceAddress = {}
        self.maskFreeSourceAddress = {}
        self.sourceMask = {'instances': 0, 'numberOfBytes': 0}
    
    # get specific data from csv file, and store them in dictionary
    def getPackets(self):
        for data in self.packetFile:
            self.packets[str(self.packetID)] = {
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
            self.packetID += 1

    # Get each packet size from packets and divide by the number of packets we have
    def getAveragePacketSize(self):
        for packet in self.packets: self.totalBytes += self.packets[packet]['packetBytes']
        self.averageSize = self.totalBytes / self.packetID
    
    def getFlowDurations(self): 
        for packet in self.packets: self.flowDurations.append(self.packets[packet]['timestampEnd'] - self.packets[packet]['timestampStart'])

    def getFlowSizes(self): 
        for packet in self.packets: self.flowSizes.append(self.packets[packet]['numberOfPackets'], self.packets[packet]['packetBytes'])
    
    def getTopSourcePorts(self):
        for packet in self.packets:
            key = self.packets[packet]['sourcePort']
            if self.sourcePorts.get(key) == None:
                self.sourcePorts[key] = 1
            else:
                self.sourcePorts[key] += 1
        self.sourcePorts = sorted(self.sourcePorts.items(), key=lambda x:x[1], reverse=True)

    def getTopDestinationPorts(self):
        for packet in self.packets:
            key = self.packets[packet]['destinationPort']
            if self.destinationPorts.get(key) == None:
                self.destinationPorts[key] = 1
            else:
                self.destinationPorts[key] += 1
        self.destinationPorts = sorted(self.destinationPorts.items(), key=lambda x:x[1], reverse=True)
    
    def mostActiveHosts(self, removeZeroMask):
        addressBook = {}         
        for packet in self.packets:
            key = self.packets[packet]['sourceAddress']
            mask = self.packets[packet]['sourceNetmask'] if removeZeroMask else -1
            if mask != 0:
                if addressBook.get(key) == None: addressBook[key] = {'instances': 1, 'numberOfBytes': self.packets[packet]['packetBytes']}
                else:
                    addressBook[key]['instances'] += 1
                    addressBook[key]['numberOfBytes'] += self.packets[packet]['packetBytes']
        addressBook = sorted(addressBook.items(), key=lambda x:x[1]['instances'], reverse=True)
        if removeZeroMask:
            self.maskFreeSourceAddress = addressBook
            return
        self.sourceAddress = addressBook
    
    def zeroMaskHosts(self):
        for packet in self.packets:
            mask = self.packets[packet]['sourceNetmask']
            if mask == 0: 
                self.sourceMask['instances'] += 1
                self.sourceMask['numberOfBytes'] += self.packets[packet]['packetBytes']
    
    #def instituteATraffic(self):

            

    
analysis = PacketManager()
analysis.getPackets()
analysis.getAveragePacketSize()
analysis.getTopSourcePorts()
analysis.getTopDestinationPorts()
analysis.mostActiveHosts(False)
analysis.mostActiveHosts(True)
analysis.zeroMaskHosts()
printAverageSize(analysis.averageSize)
printTopPorts(analysis.sourcePorts, 'Source Port', analysis.packetID)
printTopPorts(analysis.destinationPorts, 'Destination Port', analysis.packetID)
printAddressTraffic(analysis.sourceAddress, 0.001, analysis.packetID)
printAddressTraffic(analysis.sourceAddress, 0.01, analysis.packetID)
printAddressTraffic(analysis.sourceAddress, 0.1, analysis.packetID)
printMaskTraffic(analysis.sourceMask['instances'], analysis.sourceMask['numberOfBytes'],analysis.totalBytes)
printAddressTraffic(analysis.maskFreeSourceAddress, 0.001, analysis.packetID)
printAddressTraffic(analysis.maskFreeSourceAddress, 0.01, analysis.packetID)
printAddressTraffic(analysis.maskFreeSourceAddress, 0.1, analysis.packetID)




