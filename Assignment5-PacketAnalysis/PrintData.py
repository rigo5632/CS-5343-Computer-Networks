# Prints Packet Data
class PrintPacketData():
    def printAverageSize(self, average):
        print(f'A. Packet Average Size')
        print(f'* Packets Average Byte Size:\t{average:.2f}')

    def printTopPorts(self, ports, classification, totalPackets, totalBytes):
        print(f'C. {classification} (Port Number - Packet Bytes per Total Packets - Packet Bytes per Total Bytes)')
        for i in range(10):
            port, instances, packetBytes = ports[i][0], ports[i][1]['instances'], ports[i][1]['bytes']
            bytesByTotalPackets = (packetBytes/totalPackets)*100
            bytesByTotalBytes =  (packetBytes/totalBytes)*100
            print(f'\t{port}\t-\t{bytesByTotalBytes:.2f}%\t-\t{bytesByTotalBytes:.2f}%')

    def printAddressTraffic(self, addresses, limit, totalPackets, totalBytes, section):
        percentage = limit * 100
        limit = int(limit*totalPackets)
        totalTraffic = 0
        for i in range(limit): 
            if i >= len(addresses):break
            totalTraffic += addresses[i][1]['bytes']
        print(f'C.{section} {percentage}% Source Address Traffic')
        print(f'* Total Traffic: \t{totalTraffic} bytes / {totalBytes} bytes')

    def printMaskTraffic(self, numberOfBytes, totalPackets):
        print(f'C.4 Mask 0 Information')
        print(f'* Total Bytes: \t{numberOfBytes} bytes / {totalPackets} bytes')

    def printInstitutesTraffic(self, sentByInstitute, sentToInstitute, totalPackets, toatlBytes):
        sentByInstituteBytes, sentByInstitutePackets = sentByInstitute['bytes'], sentByInstitute['packets']
        sentToInstituteBytes, sentToInstitutePackets = sentToInstitute['bytes'], sentToInstitute['packets']
        print(f'* Institute A Traffic')
        print(f'- Sent By Institue A Bytes: \t{sentByInstituteBytes}/{toatlBytes} \tbytes')
        print(f'- Sent By Institue A Packets: \t{sentByInstitutePackets}/{totalPackets} \t\tpackets')
        print(f'- Sent To Institue A Bytes: \t{sentToInstituteBytes}/{toatlBytes} \tbytes')
        print(f'- Sent To Institue A Packets: \t{sentToInstitutePackets}/{totalPackets} \t\tpackets')

