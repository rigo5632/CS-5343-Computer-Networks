#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include "PacketHeader.h"

#define SIZE_ETHERNET 14

/*
* gets the packet and defines what type of packet it is
* it also prints the packet data
*/
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet){
  const struct sniff_ethernet *ethernet;
  const struct sniff_ip *ip;              
  const struct sniff_tcp *tcp;            
  const char *payload;                   

  int size_ip;
  int size_tcp;
  int size_payload;

  ethernet = (struct sniff_ethernet*)(packet);

  ip = (struct sniff_ip*)(packet + SIZE_ETHERNET);
  size_ip = IP_HL(ip)*4;
  
  // gets source up and dest ip
  printf("Source IP: %s\n", inet_ntoa(ip->ip_src));
  printf("Destination IP: %s\n", inet_ntoa(ip->ip_dst));
  
  // protocol using
  switch(ip->ip_p) {
  case IPPROTO_TCP:
    printf("Protocol: TCP\n");
    break;
  case IPPROTO_UDP:
    printf("Protocol: UDP\n");
    return;
  case IPPROTO_ICMP:
    printf("Protocol: ICMP\n");
    return;
  case IPPROTO_IP:
    printf("Protocol: IP\n");
    return;
  default:
    printf("Protocol: unknown\n");
    return;
  }
  
  // packet payload
  tcp = (struct sniff_tcp*)(packet + SIZE_ETHERNET + size_ip);
  size_tcp = TH_OFF(tcp)*4;

  payload = (u_char *)(packet + SIZE_ETHERNET + size_ip + size_tcp);
  size_payload = ntohs(ip->ip_len) - (size_ip + size_tcp);

  for(int i = 0; i < size_payload; i++){
    printf("%c", *payload);
    *payload++;
  }

  return;
}

int main(){
  int option;
  
  printf("1. Print all packets\n");
  printf("2. Apply ICMP filter\n");
  printf("3. Apply TCP filter with port ranges\n");
  printf("4. Sniff Packets\n");
  printf("$ ");
  scanf("%d", &option);
  char filter_exp[] = "";

  if(option == 2){ 
    strcpy(filter_exp, "src host 10.0.2.15 and dst host 192.168.0.11 and icmp"); 
  }
  else if(option == 3){
    int x_limit;
    int y_limit;
    printf("--------\n");
    printf("Port X -> ");
    scanf("%d", &x_limit);
    printf("---------\n");
    printf("Port Y -> ");
    scanf("%d", &y_limit);

    char filter[50];
    sprintf(filter, "dst poortrange %d-%d and tcp", x_limit, y_limit);
    strcpy(filter_exp, filter); 
  }
  else { strcpy(filter_exp, ""); }

  char errbuf[PCAP_ERRBUF_SIZE], *dev;
  pcap_t *handle;

  struct bpf_program fp;
  bpf_u_int32 mask;
  bpf_u_int32 net;
  
  // gets device from our host machine
  dev = pcap_lookupdev(errbuf);
  if (dev == NULL) {
    fprintf(stderr, "Couldn't find default device: %s\n", errbuf);
    return 1;
  }

  // configures net
  if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
    fprintf(stderr, "Couldn't get netmask for device %s: %s\n", dev, errbuf);
    net = 0;
    mask = 0;
  }
  
  // starts session
  handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
  if (handle == NULL) {
    fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
    return 1;
  }

  // adds sniffer to net
  if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) {
    fprintf(stderr, "Couldn't parse filter %s: %s\n", filter_exp, pcap_geterr(handle));
    return 1;
  }

  // adds filter if any to net
  if (pcap_setfilter(handle, &fp) == -1) {
    fprintf(stderr, "Couldn't install filter %s: %s\n", filter_exp, pcap_geterr(handle));
    return 1;
  }
  
  // listens to all packages
  pcap_loop(handle, -1, got_packet, NULL);
  pcap_close(handle);

  return 0;
}
