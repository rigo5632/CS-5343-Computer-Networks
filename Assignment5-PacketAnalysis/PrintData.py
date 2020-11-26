def printAverageSize(average):
    print(f'* Packet Average Size')
    print(f'- Packets Average Byte Size:\t{average}')

def printTopPorts(ports, classification, totalPackets):
    print(f'* {classification} (Port Number - Number of Instances - Percentage of Traffic)')
    for i in range(10):
        percentage = (ports[i][1]/totalPackets)*100
        print(f'\t{ports[i][0]}\t-\t{ports[i][1]}\t-\t{percentage:.2f} %')

def printAddressTraffic(addresses, limit, totalPackets):
    percentage = limit * 100
    limit = int(limit*totalPackets)
    print(f'* {percentage}% Source Address Traffic (Address - instances - bytes)')
    for i in range(limit):
        address, instances, numberOfBytes = addresses[i][0], addresses[i][1]['instances'], addresses[i][1]['numberOfBytes']
        print(f'\t{address}\t-\t{instances}\t-\t{numberOfBytes}\t\tbytes')

def printMaskTraffic(instances, numberOfBytes, totalPackets):
    print(f'* Mask 0 Information')
    print(f'- Instances: {instances}')
    print(f'- Total Bytes: \t{numberOfBytes}/{totalPackets}')

def printInstituesTraffic(sentByInstitute, sentToInstitute, totalPackets, toatlBytes):
    sentByInstituteBytes, sentByInstitutePackets = sentByInstitute['bytes'], sentByInstitute['packets']
    sentToInstituteBytes, sentToInstitutePackets = sentToInstitute['bytes'], sentToInstitute['packets']
    print(f'* Institute A Traffic')
    print(f'- Sent By Institue A Bytes: \t{sentByInstituteBytes}/{toatlBytes} \tbytes')
    print(f'- Sent By Institue A Packets: \t{sentByInstitutePackets}/{totalPackets} \t\tpackets')
    print(f'- Sent To Institue A Bytes: \t{sentToInstituteBytes}/{toatlBytes} \tbytes')
    print(f'- Sent To Institue A Packets: \t{sentToInstitutePackets}/{totalPackets} \t\tpackets')

