import numpy as np
import scipy.stats
import re
from matplotlib import pyplot as plt
from PrintData import PrintPacketData

class PacketManager():
    def __init__(self):
        self.packetFile             = np.genfromtxt('./Packet-Data/Netflow_dataset_small.csv', delimiter=',', dtype=None, encoding=None)
        self.totalBytes             = 0
        self.totalPackets           = 0
        self.averagePacketSize      = 0
        self.zeroMaskPackets        = 0
        self.sourcePorts            = {}
        self.destinationPorts       = {}
        self.networkTraffic         = {}
        self.filteredNetworkTraffic = {}
        self.instituteSource        = {'bytes': 0, 'packets': 0}
        self.instituteDestination   = {'bytes': 0, 'packets': 0}

    
    def extractData(self):
        for data in self.packetFile:
            packets,packetBytes,timeStampStart,timeStampEnd,sourceAddress,destinationAddress = data[4],data[5],data[6],data[7],data[10],data[11]
            sourcePort,destinationPort,protocol,sourceMask,destinationMask,sourceAutonomous,destinationAutonomous = data[15],data[16],data[17],data[20],data[21],data[22],data[23]
            self.countTotalPackets(packets)
            self.countPacketBytes(packetBytes)
            self.topSourcePorts(sourcePort,packetBytes)
            self.topDestinationPorts(destinationPort,packetBytes)
            self.mostActiveHosts(sourceAddress, packetBytes)
            self.filteredActiveHosts(sourceAddress, packetBytes, sourceMask)
            self.institutesNetworkTraffic(sourceAddress, destinationAddress, packetBytes, packets)
        self.calculateAveragePacketSize()
        self.sortSets()
    
    def calculateAveragePacketSize(self):
        self.averagePacketSize = self.totalBytes/self.totalPackets
    
    def sortSets(self):
        self.sourcePorts = sorted(self.sourcePorts.items(), key=lambda x:x[1]['instances'], reverse=True)
        self.destinationPorts = sorted(self.destinationPorts.items(), key=lambda x:x[1]['instances'], reverse=True)
        self.networkTraffic = sorted(self.networkTraffic.items(), key=lambda x:x[1]['instances'], reverse=True)
        self.filteredNetworkTraffic = sorted(self.filteredNetworkTraffic.items(), key=lambda x:x[1]['instances'], reverse=True)

    def countTotalPackets(self, numberOfPackets): 
        self.totalPackets += numberOfPackets
    
    def countPacketBytes(self, numberOfBytes): 
        self.totalBytes += numberOfBytes

    def topSourcePorts(self, port, packetBytes):
        if self.sourcePorts.get(port) == None:
            self.sourcePorts[port] = {'instances': 1, 'bytes': packetBytes}
        else:
            self.sourcePorts[port]['instances'] += 1
            self.sourcePorts[port]['bytes'] += packetBytes
        
    def topDestinationPorts(self, port, packetBytes):
        if self.destinationPorts.get(port) == None:
            self.destinationPorts[port] = {'instances': 1, 'bytes': packetBytes}
        else:
            self.destinationPorts[port]['instances'] += 1
            self.destinationPorts[port]['bytes'] += packetBytes
    
    def mostActiveHosts(self, ipAddress, packetBytes):
        if self.networkTraffic.get(ipAddress) == None:
            self.networkTraffic[ipAddress] = {'instances': 1, 'bytes': packetBytes}
        else:
            self.networkTraffic[ipAddress]['instances'] += 1
            self.networkTraffic[ipAddress]['bytes'] += packetBytes
    
    def filteredActiveHosts(self, ipAddress, packetBytes, mask):
        if mask == 0:
            self.zeroMaskPackets += packetBytes
            return
        else:
            if self.filteredNetworkTraffic.get(ipAddress) == None:
                self.filteredNetworkTraffic[ipAddress] = {'instances': 1, 'bytes': packetBytes}
            else:
                self.filteredNetworkTraffic[ipAddress]['instances'] += 1
                self.filteredNetworkTraffic[ipAddress]['bytes'] += packetBytes
    
    def institutesNetworkTraffic(self, source, destination, packetBytes, packets):
        minAddress = [128, 112, 0, 0]
        maxAddress = [128, 112, 255, 255]

        sourceAddress, destinationAddress = self.convertAddress(source, destination)

        if minAddress[0] == sourceAddress[0] and minAddress[1] == sourceAddress[1]:
            if sourceAddress[2] >= minAddress[2] and sourceAddress[3] >= minAddress[3] and sourceAddress[2] <= maxAddress[2] and sourceAddress[3] <= maxAddress[3]:
                self.instituteSource['bytes'] += packetBytes
                self.instituteSource['packets'] += packets


        if minAddress[0] ==  destinationAddress[0] and minAddress[1] ==  destinationAddress[1]:
            if  destinationAddress[2] >= minAddress[2] and  destinationAddress[3] >= minAddress[3] and  destinationAddress[2] <= maxAddress[2] and  destinationAddress[3] <= maxAddress[3]:
                self.instituteDestination['bytes'] += packetBytes
                self.instituteDestination['packets'] += packets

    
    def convertAddress(self, sourceAddress, destinationAddress):
        sourceAddress = re.split('\.', sourceAddress)
        destinationAddress = re.split('\.', destinationAddress)

        for i in range(4):
            sourceAddress[i] = int(sourceAddress[i])
            destinationAddress[i] = int(destinationAddress[i])
        
        return sourceAddress, destinationAddress

     
analysis = PacketManager()
packet = PrintPacketData()
analysis.extractData()

packet.printAverageSize(analysis.averagePacketSize)
packet.printTopPorts(analysis.sourcePorts, 'Source Ports', analysis.totalPackets, analysis.totalBytes)
packet.printTopPorts(analysis.destinationPorts, 'Destination Ports', analysis.totalPackets, analysis.totalBytes)
packet.printAddressTraffic(analysis.networkTraffic, 0.001, analysis.totalPackets, analysis.totalBytes, 1)
packet.printAddressTraffic(analysis.networkTraffic, 0.01, analysis.totalPackets, analysis.totalBytes, 2)
packet.printAddressTraffic(analysis.networkTraffic, 0.1, analysis.totalPackets, analysis.totalBytes, 3)
packet.printMaskTraffic(analysis.zeroMaskPackets, analysis.totalBytes)
packet.printAddressTraffic(analysis.filteredNetworkTraffic, 0.001, analysis.totalPackets, analysis.totalBytes, 5.1)
packet.printAddressTraffic(analysis.filteredNetworkTraffic, 0.01, analysis.totalPackets, analysis.totalBytes, 5.2)
packet.printAddressTraffic(analysis.filteredNetworkTraffic, 0.1, analysis.totalPackets, analysis.totalBytes, 5.3)
packet.printInstitutesTraffic(analysis.instituteSource, analysis.instituteDestination, analysis.totalPackets, analysis.totalBytes)







