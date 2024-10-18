from scapy.all import *

def dns_lookup(domaine):
    ans = sr1(
        IP(dst="8.8.8.8") /
        UDP(sport=RandShort(), dport=53) /
        DNS(rd=1, qd=DNSQR(qname=domaine, qtype="A"))
    )
    print("L'une des ip de", domaine,"est:", ans.an[0].rdata)

domaine = "ynov.com"

dns_lookup(domaine)
