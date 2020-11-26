def printAverageSize(average):
    print(f'* Average Size: \t{average}')

def printTopPorts(ports, classification, totalPackets):
    print(f'* {classification} (Port Number - Number of Instances - Percentage of Traffic)')
    for i in range(10):
        percentage = (ports[i][1]/totalPackets)*100
        print(f'\t{ports[i][0]}\t-\t{ports[i][1]}\t-\t{percentage:.2f} %')

def printAddressTraffic(addresses, limit, totalPackets):
    percentage = limit * 100
    limit = int(limit*totalPackets)
    print(f'* {percentage}% Source Address Traffic (Address - (instances: #, number of bytes: #))')
    for i in range(limit):
        print(f'\t{addresses[i][0]}\t-\t{addresses[i][1]}')

def printMaskTraffic(instances, numberOfBytes, totalPackets):
    print(f'* Mask 0 Instances: \t{instances}')
    print(f'* Mask 0 Total Bytes: \t{numberOfBytes}/{totalPackets}')

def printInstituesTraffic(sentByInstitute, sentToInstitute, totalPackets, toatlBytes):
    sentByInstituteBytes, sentByInstitutePackets = sentByInstitute['bytes'], sentByInstitute['packets']
    sentToInstituteBytes, sentToInstitutePackets = sentToInstitute['bytes'], sentToInstitute['packets']
    print(f'* Institute A Traffic')
    print(f'* Sent By Institue A Bytes: \t{sentByInstituteBytes}/{toatlBytes} \tbytes')
    print(f'* Sent By Institue A Packets: \t{sentByInstitutePackets}/{totalPackets} \t\tpackets')
    print(f'* Sent To Institue A Bytes: \t{sentToInstituteBytes}/{toatlBytes} \tbytes')
    print(f'* Sent To Institue A Packets: \t{sentToInstitutePackets}/{totalPackets} \t\tpackets')

