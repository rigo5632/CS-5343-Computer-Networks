#! /usr/bin/python3

#import numpy
import scipy.stats
from matplotlib import pyplot as plt

class PacketManager():
    def __init__(self):
        self.packetFile = np.genfromtxt('./Packet-Data/Netflow_dataset.csv', delimiter=',')
        self.packets = {}
        self.packetID = 1
        self.packetSizes = 0
        self.flowDurations = []
        self.flowSizes = []
    
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
        for packet in self.packets: self.packetSizes += self.packets[packet]['packetBytes']
        self.packetSizes // packetID
    
    def getFlowDurations(self):
        if self.flowDurations is None: return
        for packet in self.packets: self.flowDurations.append(self.packets[packet]['timestampEnd'] - self.packets[packet]['timestampStart'])

    def getFlowSizes(self):
        if self.flowSizes is None: return
        for packet in self.packets: self.flowSizes.append(self.packets[packet]['numberOfPackets'], self.packets[packet]['packetBytes'])

    def createCCDF(data):
        Year = [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]
        Unemployment_Rate = [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        
        plt.plot(Year, Unemployment_Rate)
        plt.title('Unemployment Rate Vs Year')
        plt.xlabel('Year')
        plt.ylabel('Unemployment Rate')
        plt.show()
        # x = np.random.randn(10000) # generate samples from normal distribution (discrete data)
        # print(x)
        # norm_cdf = scipy.stats.norm.cdf(x) # calculate the cdf - also discrete

        # plt.plot(x, norm_cdf)
        # plt.show()
        # print('hey')

analysis = PacketManager()
analysis.createCCDF()

