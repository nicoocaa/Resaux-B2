from scapy.all import *

def print_dns(packet):
        if (packet[DNSQR].qname.decode().rstrip('.')) == 'ynov.com':
            for i in range(packet[DNS].ancount):
                answer = packet[DNSRR][i]
                if answer.type == 1:
                    print(f"DNS Answer {answer.rdata}")

sniff(filter="port 53", prn=print_dns)
