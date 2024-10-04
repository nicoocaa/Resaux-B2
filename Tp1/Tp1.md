# TP1 : Maîtrise réseau du votre poste

# I. Basics

☀️ **Carte réseau WiFi**

Déterminer...

- l'adresse MAC de votre carte WiFi: 
```Adresse physique . . . . . . . . . . . : C8-5E-A9-3E-3E-FB```
- l'adresse IP de votre carte WiFi : 
```Adresse IPv4. . . . . . . . . . . . . .: 10.33.73.226```
- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
  - en notation CIDR, par exemple `10.33.73.226☀️/20☀️`
  - ET en notation décimale:  `Masque de sous-réseau. . . . . . . . . : 255.255.240.00`

---

☀️ **Déso pas déso**

Pas besoin d'un terminal là, juste une feuille, ou votre tête, ou un tool qui calcule tout hihi. Déterminer...

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi : ```10.33.64.0```
- l'adresse de broadcast : ```10.33.73.255```
- le nombre d'adresses IP disponibles dans ce réseau: ```4094```

---

☀️ **Hostname**

```Nom de l’hôte . . . . . . . . . . : BOOK-SH7AR92TBB```

---

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau : ```10.33.79.254```
- l'adresse MAC de la passerelle du réseau : 
```arp -a``` 
``` 7c-5a-1c-d3-d8-76 ```

---

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP : 
 ```10.33.79.254```
- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet
```Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8```
---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut :

```
PS C:\Users\nicop> route print
===========================================================================
Liste d'Interfaces
  2...00 ff 01 78 25 50 ......TAP-Windows Adapter V9 for OpenVPN Connect
  3...0a 00 27 00 00 03 ......VirtualBox Host-Only Ethernet Adapter
 12...........................OpenVPN Data Channel Offload
 20...c8 5e a9 3e 3e fc ......Microsoft Wi-Fi Direct Virtual Adapter
 17...ca 5e a9 3e 3e fb ......Microsoft Wi-Fi Direct Virtual Adapter #2
  7...c8 5e a9 3e 3e fb ......Intel(R) Wi-Fi 6E AX211 160MHz
  1...........................Software Loopback Interface 1
===========================================================================

IPv4 Table de routage
===========================================================================
Itinéraires actifs :
Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
          0.0.0.0          0.0.0.0     ☀️10.33.79.254 ☀️    10.33.73.226     30
         10.1.1.0    255.255.255.0         On-link          10.1.1.1    281
         10.1.1.1  255.255.255.255         On-link          10.1.1.1    281
       10.1.1.255  255.255.255.255         On-link          10.1.1.1    281
       10.33.64.0    255.255.240.0         On-link      10.33.73.226    286
     10.33.73.226  255.255.255.255         On-link      10.33.73.226    286
     10.33.79.255  255.255.255.255         On-link      10.33.73.226    286
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    331
        127.0.0.1  255.255.255.255         On-link         127.0.0.1    331
  127.255.255.255  255.255.255.255         On-link         127.0.0.1    331
        224.0.0.0        240.0.0.0         On-link         127.0.0.1    331
        224.0.0.0        240.0.0.0         On-link          10.1.1.1    281
        224.0.0.0        240.0.0.0         On-link      10.33.73.226    286
  255.255.255.255  255.255.255.255         On-link         127.0.0.1    331
  255.255.255.255  255.255.255.255         On-link          10.1.1.1    281
  255.255.255.255  255.255.255.255         On-link      10.33.73.226    286
===========================================================================
Itinéraires persistants :
  Aucun

IPv6 Table de routage
===========================================================================
Itinéraires actifs :
 If Metric Network Destination      Gateway
  1    331 ::1/128                  On-link
  3    281 fe80::/64                On-link
  7    286 fe80::/64                On-link
  3    281 fe80::1a15:b4ba:793b:551a/128
                                    On-link
  7    286 fe80::f37b:1af1:5fff:8ce2/128
                                    On-link
  1    331 ff00::/8                 On-link
  3    281 ff00::/8                 On-link
  7    286 ff00::/8                 On-link
===========================================================================
Itinéraires persistants :
  Aucun
```

---

# II. Go further

---

☀️ **Hosts ?**

```PS C:\Users\nicop> ping b2.hello.vous

Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=19 ms TTL=55
Réponse de 1.1.1.1 : octets=32 temps=20 ms TTL=55
Réponse de 1.1.1.1 : octets=32 temps=18 ms TTL=55
Réponse de 1.1.1.1 : octets=32 temps=19 ms TTL=55

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 18ms, Maximum = 20ms, Moyenne = 19ms
PS C:\Users\nicop>```

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo : ``` 188.114.97.7 ```
- le port du serveur auquel vous êtes connectés : ``` 443 ```
- le port que votre PC a ouvert en local pour se connecter au port du serveur distant  : ```562559```


---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.thinkerview.com`

```PS C:\Users\nicop> nslookup www.thinkerview.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    www.thinkerview.com
Addresses:  2a06:98c1:3121::7
          2a06:98c1:3120::7
          ☀️188.114.96.☀️
          ☀️188.114.97.7☀️
```


- à quel nom de domaine correspond l'IP `143.90.88.12`

```PS C:\Users\nicop> nslookup 143.90.88.12
Serveur :   dns.google
Address:  8.8.8.8

☀️ Nom :    EAOcf-140p12.ppp15.odn.ne.jp☀️
Address:  143.90.88.12

```

---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com` : 8

```PS C:\Users\nicop> tracert www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [172.67.74.226]
avec un maximum de 30 sauts :

  1     4 ms     2 ms     2 ms  10.33.79.254
  2     4 ms     3 ms     5 ms  145.117.7.195.rev.sfr.net [195.7.117.145]
  3     5 ms     3 ms     4 ms  237.195.79.86.rev.sfr.net [86.79.195.237]
  4     7 ms     4 ms     6 ms  196.224.65.86.rev.sfr.net [86.65.224.196]
  5    14 ms    11 ms    11 ms  164.147.6.194.rev.sfr.net [194.6.147.164]
  6    21 ms     *       20 ms  162.158.20.24
  7    26 ms    25 ms    17 ms  162.158.20.240
  8    19 ms    15 ms    17 ms  172.67.74.226

Itinéraire déterminé.```

---

☀️ **IP publique**

Déterminer...


- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

```PS C:\Users\nicop> (Invoke-WebRequest ifconfig.me/ip).Content
195.7.117.146```

# III. Le requin

Faites chauffer Wireshark. Pour chaque point, je veux que vous me livrez une capture Wireshark, format `.pcap` donc.

Faites *clean* 🧹, vous êtes des grands now :

- livrez moi des captures réseau avec uniquement ce que je demande et pas 40000 autres paquets autour
  - vous pouvez sélectionner seulement certains paquets quand vous enregistrez la capture dans Wireshark
- stockez les fichiers `.pcap` dans le dépôt git et côté rendu Markdown, vous me faites un lien vers le fichier, c'est cette syntaxe :

```markdown
[Lien vers capture ARP](./captures/arp.pcap)
```

---

☀️ **Capture ARP**

- [ 📁 fichier `arp.pcap`](./arp.pcap) 
---

☀️ **Capture DNS**

- [ 📁 fichier `dns.pcap`](./dns.pcap)


---

☀️ **Capture TCP**

- [ 📁 fichier `tcp.pcap`](./tcp.pcap)

---
