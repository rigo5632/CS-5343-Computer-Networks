import numpy as np
import csv
import math
import re
from matplotlib import pyplot as plt
from PrintData import PrintPacketData

class PacketManager():
    def __init__(self):
        self.packetFile             = './Packet-Data/Netflow_dataset.csv'
        self.totalPackets           = 0
        self.totalBytes             = 0
        self.graphData              = {'durations':[], 'sizes':[]}
        self.topSourcePorts         = {}
        self.topDestinationPorts    = {}
        self.popularHosts           = {}
        self.zeroMaskHosts          = {'instances': 0, 'totalBytes': 0}
        self.filteredPopularHosts   = {}
        self.instituteSource        = {'instances': 0, 'totalBytes': 0, 'totalPackets': 0}
        self.instituteDestination   = {'instances': 0, 'totalBytes': 0, 'totalPackets': 0}
    
    def extractFileData(self):
        with open(self.packetFile, 'r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            next(csvReader)
            for data in csvReader:
                packets, packetBytes = int(data[4]), int(data[5])
                self.totalPackets += packets
                self.totalBytes += packetBytes
                self.sourcePorts(data[15], packetBytes)
                self.destinationPorts(data[16], packetBytes)
                self.activeHosts(data[10], packetBytes)
                self.recordZeroMaskHost(data[20], packetBytes)
                self.filterActiveHosts(data[10], packetBytes, data[20])
                self.instituteInformation(data[10], data[11], packetBytes, packets)
                self.graphData['durations'].append(int(data[7]) - int(data[6]))
                self.graphData['sizes'].append(packetBytes/packets)
        
    def generateLinearDurationGraph(self):
        figure1 = plt.figure(1)

        x = np.sort(self.graphData['durations'])
        y = 1 - (np.array(range(len(self.graphData['durations'])))/float(len(self.graphData['durations'])))

        plt.title('Linera Duration Graph')
        plt.plot(x, y)
    
    def generateLogDurationsGraph(self):
        figure2 =  plt.figure(2)
        sortedX = np.sort(self.graphData['durations'])
        x = [math.log(sortedX[i]) if sortedX[i] > 0 else 0 for i in range(len(sortedX))]
        y = 1 - (np.array(range(len(x))))/float(len(x))

        plt.title('Log Duration Graph')
        plt.plot(x, y)
    
    def generateLinearSizeGraph(self):
        figure3 = plt.figure(3)

        x = np.sort(self.graphData['sizes'])
        y = 1 - (np.array(range(len(self.graphData['sizes']))))/float(len(self.graphData['sizes']))

        plt.title('Linear Size Graph')
        plt.plot(x, y)
    
    def generateLogSizeGraph(self):
        figure4 = plt.figure(4)
        sortedX = np.sort(self.graphData['sizes'])
        x = [math.log(sortedX[i]) if sortedX[i] > 0 else 0 for i in range(len(sortedX))]
        y = 1 - (np.array(range(len(x))))/float(len(x))

        plt.title('Log Size Graph')
        plt.plot(x, y)
            
    def averagePacketSize(self): 
        return self.totalBytes / self.totalPackets
    
    def sourcePorts(self, port, packetBytes):
        if self.topSourcePorts.get(port) == None:
            self.topSourcePorts[port] = {'instances': 1, 'totalBytes': packetBytes}
            return
        else:
            self.topSourcePorts[port]['instances'] += 1
            self.topSourcePorts[port]['totalBytes'] += packetBytes
        return
    
    def destinationPorts(self, port, packetBytes):
        if self.topDestinationPorts.get(port) == None:
            self.topDestinationPorts[port] = {'instances': 1, 'totalBytes': packetBytes}
            return
        else:
            self.topDestinationPorts[port]['instances'] += 1
            self.topDestinationPorts[port]['totalBytes'] += packetBytes
        return
    
    def activeHosts(self, ipAddress, packetBytes):
        if self.popularHosts.get(ipAddress) == None:
            self.popularHosts[ipAddress] = {'instances': 1, 'totalBytes': packetBytes}
            return
        else:
            self.popularHosts[ipAddress]['instances'] += 1
            self.popularHosts[ipAddress]['totalBytes'] += packetBytes
        return
    
    def recordZeroMaskHost(self, mask, packetBytes):
        if mask == 0:
            self.zeroMaskHosts['instances'] += 1
            self.zeroMaskHosts['totalBytes'] += packetBytes
        return
    
    def filterActiveHosts(self, ipAddress, packetBytes, mask):
        if mask == 0:
            return
        if self.filteredPopularHosts.get(ipAddress) == None:
            self.filteredPopularHosts[ipAddress] = {'instances': 1, 'totalBytes': packetBytes}
        else:
            self.filteredPopularHosts[ipAddress]['instances'] += 1
            self.filteredPopularHosts[ipAddress]['totalBytes'] += packetBytes
    
    def instituteInformation(self, sourceAddress, destinationAddress, packetBytes, packets):
        source, destination = self.extractAddress(sourceAddress, destinationAddress)

        if source[0] == 128 and source[1] == 112 and source[2] >= 0 and source[3] >= 0 and source[2] <= 255 and source[3] <= 255:
            self.instituteSource['instances'] += 1
            self.instituteSource['totalBytes'] += packetBytes
            self.instituteSource['totalPackets'] += packets

        if destination[0] == 128 and destination[1] == 112 and destination[2] >= 0 and destination[3] >= 0 and destination[2] <= 255 and destination[3] <= 255:
            self.instituteDestination['instances'] += 1
            self.instituteDestination['totalBytes'] += packetBytes
            self.instituteDestination['totalPackets'] += packets

    def extractAddress(self, source, destination):
        sourceAddress = re.split('\.', source)
        destinationAddress = re.split('\.', destination)

        for i in range(4):
            sourceAddress[i] = int(sourceAddress[i])
            destinationAddress[i] = int(destinationAddress[i])
        
        return sourceAddress, destinationAddress
    
    def sortTopPorts(self):
        return (sorted(self.topSourcePorts.items(), key=lambda x:x[1]['totalBytes'], reverse=True),
        sorted(self.topDestinationPorts.items(), key=lambda x:x[1]['totalBytes'], reverse=True),
        sorted(self.popularHosts.items(), key=lambda x:x[1]['instances'], reverse=True),
        sorted(self.filteredPopularHosts.items(), key=lambda x:x[1]['instances'], reverse=True))


analysis = PacketManager()
packet = PrintPacketData()
analysis.extractFileData()
analysis.generateLinearDurationGraph()
analysis.generateLogDurationsGraph()
analysis.generateLinearSizeGraph()
analysis.generateLogSizeGraph()
sortedSourcePorts, sortedDestinationPorts, sortedPopularHosts, sortedFilteredHosts = analysis.sortTopPorts()

packet.printAveragePacketSize(analysis.averagePacketSize())
packet.printTopPorts('Source Ports', sortedSourcePorts, analysis.totalPackets, analysis.totalBytes)
packet.printTopPorts('Destination Ports', sortedDestinationPorts, analysis.totalPackets, analysis.totalBytes)
packet.printAddressTraffic(sortedPopularHosts, 0.001, analysis.totalBytes)
packet.printAddressTraffic(sortedPopularHosts, 0.01, analysis.totalBytes)
packet.printAddressTraffic(sortedPopularHosts, 0.1, analysis.totalBytes)
packet.printZeroMaskTraffic(analysis.zeroMaskHosts, analysis.totalBytes)
packet.printAddressTraffic(sortedFilteredHosts, 0.001, analysis.totalBytes)
packet.printAddressTraffic(sortedFilteredHosts, 0.01, analysis.totalBytes)
packet.printAddressTraffic(sortedFilteredHosts, 0.1, analysis.totalBytes)
packet.printInstituteTraffic(analysis.instituteSource, analysis.instituteDestination, analysis.totalPackets, analysis.totalBytes)
plt.show()