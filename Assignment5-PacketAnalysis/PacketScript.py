import numpy as np
import scipy.stats
from matplotlib import pyplot as plt
from PrintData import printAverageSize, printTopPorts

class PacketManager():
    def __init__(self):
        self.packetFile = np.genfromtxt('./Packet-Data/Netflow_dataset_small.csv', delimiter=',')
        self.packets = {}
        self.packetID = 1
        self.averageSize = 0
        self.flowDurations = []
        self.flowSizes = []
        self.sourcePorts = {}
        self.destinationPorts = {}
    
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
        if self.packets is None: return
        for packet in self.packets: self.averageSize += self.packets[packet]['packetBytes']
        self.averageSize /= self.packetID
    
    def getFlowDurations(self):
        if self.flowDurations is None: return
        for packet in self.packets: self.flowDurations.append(self.packets[packet]['timestampEnd'] - self.packets[packet]['timestampStart'])

    def getFlowSizes(self):
        if self.flowSizes is None: return
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
    
    
    def createCCDF(self):
        plt.plot()
        plt.title('Number of Packets vs Packet Sizes')
        plt.xlabel('Number of Packets')
        plt.ylabel('Packet Sizes')
        plt.show()
        # x = np.random.randn(10000) # generate samples from normal distribution (discrete data)
        # print(x)
        # norm_cdf = scipy.stats.norm.cdf(x) # calculate the cdf - also discrete

        # plt.plot(x, norm_cdf)
        # plt.show()
        # print('hey')
    

analysis = PacketManager()
analysis.getPackets()
analysis.getAveragePacketSize()
analysis.getTopSourcePorts()
analysis.getTopDestinationPorts()
printAverageSize(analysis.averageSize)
printTopPorts(analysis.sourcePorts, 'Source Port', analysis.packetID)
printTopPorts(analysis.destinationPorts, 'Destination Port', analysis.packetID)


