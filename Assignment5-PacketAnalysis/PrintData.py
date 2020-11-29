class PrintPacketData():
    def printAveragePacketSize(self, average):
        print(f'A. Packet Average Size: {average:.2f} bytes/packet')
    
    def printTopPorts(self, type, ports, totalPackets, totalBytes):
        print(f'C. Top 10 {type} (Port Number - Total Bytes Percentage)')
        for i in range(10):
            port, instances, packetBytes = ports[i][0], ports[i][1]['instances'], ports[i][1]['totalBytes']
            totalPacketsPercentage, totalBytesPercentage = (instances/totalPackets)*100, (packetBytes/totalBytes)*100
            print(f'\t{port}\t-\t{totalBytesPercentage:.2f}%')
    
    def printAddressTraffic(self, addresses, limit, totalBytes):
        percentage = limit * 100
        limit = int(limit*len(addresses))
        totalTraffic = 0

        for i in range(limit): totalTraffic += addresses[i][1]['totalBytes']

        print(f'D. {percentage}% Source Address Traffic')
        print(f'* Total Traffic: \t{totalTraffic} bytes / {totalBytes} bytes')
    
    def printZeroMaskTraffic(self, mask, totalBytes):
        maskBytes = mask['totalBytes']
        print(f'D. Mask 0 Information')
        print(f'* Total Bytes: \t{maskBytes} bytes / {totalBytes} bytes')
    
    def printInstituteTraffic(self, sentByInstitute, sentToInstitute, totalPackets, totalBytes):
        sentByBytes, sentByPackets = sentByInstitute['totalBytes'], sentByInstitute['totalPackets']
        sentToBytes, sentToPackets = sentToInstitute['totalBytes'], sentToInstitute['totalPackets']
        print('E. Institute A Traffic')
        print(f'* Sent By Institue A Bytes: \t{sentByBytes} / {totalBytes} \tbytes')
        print(f'* Sent By Institue A Packets: \t{sentByPackets} / {totalPackets} \t\tpackets')
        print(f'* Sent To Institue A Bytes: \t{sentToBytes} / {totalBytes} \tbytes')
        print(f'* Sent To Institue A Packets: \t{sentToPackets} / {totalPackets} \t\tpackets')
