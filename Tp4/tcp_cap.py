from scapy.all import sniff

def print_tcp(packet):
    ip_layer = packet['IP']
    tcp_layer = packet['TCP']
    print("TCP SYN ACK reçu !")
    print(f"- Adresse IP src : {ip_layer.src}")
    print(f"- Adresse IP dest : {ip_layer.dst}")
    print(f"- Port TCP src : {tcp_layer.sport}")
    print(f"- Port TCP dst : {tcp_layer.dport}")


sniff(filter="tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack != 0", prn=print_tcp, count=1)