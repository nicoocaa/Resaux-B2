
from scapy.all import *

ping = ICMP(type=8)

packet = IP(src="10.33.73.226", dst="10.33.67.174")  #vu que l'ip de la passerelle ne peut pas étre ping j'ai ping Stan

frame = Ether(src="c8:5e:a9:3e:3e:fb", dst="f2:39:c5:c0:07:e5")


final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")
