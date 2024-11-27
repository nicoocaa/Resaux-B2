# TP7 SECU : Accès réseau sécurisé

## Sommaire

- [TP7 SECU : Accès réseau sécurisé](#tp7-secu--accès-réseau-sécurisé)
  - [Sommaire](#sommaire)
- [I. VPN](#i-vpn)
- [II. SSH](#ii-ssh)
  - [1. Setup](#1-setup)
  - [2. Bastion](#2-bastion)
  - [3. Connexion par clé](#3-connexion-par-clé)
  - [4. Conf serveur SSH](#4-conf-serveur-ssh)
- [III. HTTP](#iii-http)
  - [1. Initial setup](#1-initial-setup)
  - [2. Génération de certificat et HTTPS](#2-génération-de-certificat-et-https)
    - [A. Préparation de la CA](#a-préparation-de-la-ca)
    - [B. Génération du certificat pour le serveur web](#b-génération-du-certificat-pour-le-serveur-web)
    - [C. Bonnes pratiques RedHat](#c-bonnes-pratiques-redhat)
    - [D. Config serveur Web](#d-config-serveur-web)
    - [E. Bonus renforcement TLS](#e-bonus-renforcement-tls)


# I. VPN


🌞 **Monter un serveur VPN Wireguard sur `vpn.tp7.secu`**

```bash
[nico@localhost ~]$ sudo systemctl start wg-quick@wg0.service
[sudo] password for nico: 
[nico@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fd:e4:32 brd ff:ff:ff:ff:ff:ff
    inet 10.7.1.100/24 brd 10.7.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fefd:e432/64 scope link 
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:1b:d8:4d brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s8
       valid_lft 417sec preferred_lft 417sec
    inet6 fe80::6025:1b6e:3379:36de/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
4: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.7.2.0/24 scope global wg0
       valid_lft forever preferred_lft forever
[nico@localhost ~]$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=56 time=14.6 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=56 time=43.8 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=56 time=24.4 ms
^C
--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/mdev = 14.629/27.585/43.756/12.106 ms
[nico@localhost ~]$ 
```

🌞 **Client Wireguard sur `martine.tp7.secu`**

```bash
[nico@localhost wireguard]$ wg-quick up ./john.conf
wg-quick must be run as root. Please enter the password for nico to continue: 
Warning: `/home/nico/wireguard/john.conf' is world accessible
[#] ip link add john type wireguard
[#] wg setconf john /dev/fd/63
[#] ip -4 address add 10.7.2.11/24 dev john
[#] ip link set mtu 1420 up dev john
[#] wg set john fwmark 51820
[#] ip -4 route add 0.0.0.0/0 dev john table 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] nft -f /dev/fd/63
[nico@localhost wireguard]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:47:b8:02 brd ff:ff:ff:ff:ff:ff
    inet 10.7.1.11/24 brd 10.7.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe47:b802/64 scope link 
       valid_lft forever preferred_lft forever
3: john: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.7.2.11/24 scope global john
       valid_lft forever preferred_lft forever
[nico@localhost wireguard]$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=55 time=15.9 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=55 time=17.8 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=55 time=16.7 ms
^C
--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 15.894/16.810/17.849/0.802 ms
[nico@localhost wireguard]$ 

```

🌞 **Client Wireguard sur votre PC**

```bash
nico@debian:~$ sudo apt install wireguard-tools
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following package was automatically installed and is no longer required:
  linux-image-6.1.0-25-amd64
Use 'sudo apt autoremove' to remove it.
Suggested packages:
  openresolv | resolvconf
The following NEW packages will be installed:
  wireguard-tools
0 upgraded, 1 newly installed, 0 to remove and 88 not upgraded.
Need to get 87.6 kB of archives.
After this operation, 329 kB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bookworm/main amd64 wireguard-tools amd64 1.0.20210914-1+b1 [87.6 kB]
Fetched 87.6 kB in 0s (1,163 kB/s)   
Selecting previously unselected package wireguard-tools.
(Reading database ... 249243 files and directories currently installed.)
Preparing to unpack .../wireguard-tools_1.0.20210914-1+b1_amd64.deb ...
Unpacking wireguard-tools (1.0.20210914-1+b1) ...
Setting up wireguard-tools (1.0.20210914-1+b1) ...
wg-quick.target is a disabled or a static unit, not starting it.
Processing triggers for man-db (2.11.2-2) ...
nico@debian:~$ mkdir wireguard
nico@debian:~$ cd wireguard/
nico@debian:~/wireguard$ wg genkey | tee john.key | wg pubkey > john.pub
nico@debian:~/wireguard$ sudo vi john.conf
nico@debian:~/wireguard$ cat john.pub 
Rzda0QzKZY6rh00EbmlOBlmUsHF1zWA6EXrkrUfxeDs=
nico@debian:~/wireguard$ wg-quick up ./john.conf
Warning: `/home/nico/wireguard/john.conf' is world accessible
[#] ip link add john type wireguard
[#] wg setconf john /dev/fd/63
[#] ip -4 address add 10.7.2.100/24 dev john
[#] ip link set mtu 1420 up dev john
[#] wg set john fwmark 51820
[#] ip -4 route add 0.0.0.0/0 dev john table 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] nft -f /dev/fd/63
nico@debian:~/wireguard$ ping 10.7.2.11
PING 10.7.2.11 (10.7.2.11) 56(84) bytes of data.
64 bytes from 10.7.2.11: icmp_seq=1 ttl=63 time=4.39 ms
64 bytes from 10.7.2.11: icmp_seq=2 ttl=63 time=3.48 ms
64 bytes from 10.7.2.11: icmp_seq=3 ttl=63 time=3.26 ms
64 bytes from 10.7.2.11: icmp_seq=4 ttl=63 time=2.58 ms
^C
--- 10.7.2.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 2.578/3.428/4.393/0.649 ms
nico@debian:~/wireguard$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: wlo1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether c8:5e:a9:3e:3e:fb brd ff:ff:ff:ff:ff:ff
    altname wlp0s20f3
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic noprefixroute wlo1
       valid_lft 42281sec preferred_lft 42281sec
    inet6 2a01:e0a:141:d7e0:4c6a:bea5:5ecb:f4c0/64 scope global dynamic noprefixroute 
       valid_lft 86245sec preferred_lft 86245sec
    inet6 fe80::b7be:d1bf:f173:b835/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: vboxnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 0a:00:27:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.7.1.1/24 brd 10.7.1.255 scope global vboxnet0
       valid_lft forever preferred_lft forever
    inet6 fe80::800:27ff:fe00:0/64 scope link 
       valid_lft forever preferred_lft forever
4: vboxnet1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 0a:00:27:00:00:01 brd ff:ff:ff:ff:ff:ff
5: john: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.7.2.100/24 scope global john
       valid_lft forever preferred_lft forever
nico@debian:~/wireguard$ 

```

➜ **A partir de ce moment dans le TP**

- toutes les machines doivent être connectées au VPN
- toutes les machines récupèrent un accès internet en passant par le réseau VPN (à part votre PC bien sûr)

🌞 **Ecrire un script `client.sh`**

[client.sh](./client.sh)
# II. SSH

## 1. Setup

🌞 **Générez des confs Wireguard pour tout le monde**

voici le script qui génére la conf client pour le bastion :

```bash
[nico@bastion ~]$ ./client.sh 
Tout les prérequis sont présent la configuration va commencer
Quelles est l'ip que vous voulez atribuer au client
Format de l'ip 10.10.10.10/24 requis

10.7.2.12/24---------------------------------------------------------------------------------------------
Veuillez ajouter les lignes suivantes au fichier de configuration de votre serveur VPN (/etc/wireguard/wg0.conf) :


[Peer]
PublicKey = rs7YI0sFaFy1iRoxV1f/AP3FQ18gDPS2dt14GatFmiU=
AllowedIPs = 
---------------------------------------------------------------------------------------------
 Aprés avoir édité le fichier de conf de votre vpn vous pouver lancer les commandes suivante 
vpn-C  pour vous connecter au vpn 
vpn-D pour vous déconecter du vpn 
[nico@bastion ~]$ rm -rf wireguard/
[nico@bastion ~]$ ./client.sh 
Tout les prérequis sont présent la configuration va commencer
Quelles est l'ip que vous voulez atribuer au client
Format de l'ip 10.10.10.10/24 requis
10.7.2.12/24
---------------------------------------------------------------------------------------------
Veuillez ajouter les lignes suivantes au fichier de configuration de votre serveur VPN (/etc/wireguard/wg0.conf) :


[Peer]
PublicKey = NfuerxwuveijY7LYb1zPAajoulyOhUYj2SbugPKqVWw=
AllowedIPs = 10.7.2.12/24
---------------------------------------------------------------------------------------------
 Aprés avoir édité le fichier de conf de votre vpn vous pouver lancer les commandes suivante 
vpn-C  pour vous connecter au vpn 
vpn-D pour vous déconecter du vpn 
[nico@bastion ~]$ 
```
c'est exactemetn la méme chose pour le web 

on peut voir que je peux ping tout le monde depuis mon pc :

```bash
nico@debian:~/wireguard$ ping 10.7.2.11
PING 10.7.2.0 (10.7.2.0) 56(84) bytes of data.
64 bytes from 10.7.2.11: icmp_seq=1 ttl=64 time=1.13 ms
64 bytes from 10.7.2.11: icmp_seq=2 ttl=64 time=1.35 ms
64 bytes from 10.7.2.11: icmp_seq=3 ttl=64 time=1.42 ms
64 bytes from 10.7.2.11: icmp_seq=4 ttl=64 time=1.24 ms
^C
--- 10.7.2.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.130/1.283/1.417/0.109 ms
nico@debian:~/wireguard$ ^C
nico@debian:~/wireguard$ ping 10.7.2.12
64 bytes from 10.7.2.12: icmp_seq=1 ttl=62 time=3.54 ms
64 bytes from 10.7.2.12: icmp_seq=2 ttl=62 time=4.90 ms
^C
--- 10.7.2.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 3.537/4.218/4.899/0.681 ms

```


## 2. Bastion


🌞 **Empêcher la connexion SSH directe sur `web.tp7.secu`**

```bash
[nico@bastion ~]$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.7.2.12" port port="22" protocol="tcp" accept'
[sudo] password for nico: 
success
[nico@bastion ~]$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" port port="22" protocol="tcp" drop'
success
[nico@bastion ~]$ sudo firewall-cmd --reload
success
[nico@bastion ~]$ 

```

🌞 **Connectez-vous avec un jump SSH**

```bash
[nico@debian ~]$ ssh -J 10.7.2.13 10.7.2.114
nico@10.7.2.13's password: 
nico@10.7.2.114's password: 
Last login: Wed Nov 27 11:10:12 2024 from 10.7.1.1
[nico@web ~]$ 
```
## 3. Connexion par clé

🌞 **Générez une nouvelle paire de clés pour ce TP**

```bash
nico@debian:~/wireguard$ ssh-keygen -t ed25519 -C "tp7-secu@nicolas" -f ~/.ssh/id_ed25519_tp7
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/nico/.ssh/id_ed25519_tp7
Your public key has been saved in /home/nico/.ssh/id_ed25519_tp7.pub
The key fingerprint is:
SHA256:69eh7N8rfGLrpSpPEVr8ePeU/NE0X47Nl3fMkfoxZes tp7-secu@nicolas
The key's randomart image is:
+--[ED25519 256]--+
|                 |
|         .      .|
|          +    +=|
|         o +  oX@|
|        S o o.oO&|
|         . o..ooO|
|        ...+ ..Eo|
|       ...+ *+.  |
|        .=+===o. |
+----[SHA256]-----+
nico@debian:~/wireguard$ 

```
## 4. Conf serveur SSH

🌞 **Changez l'adresse IP d'écoute**

```bash
[nico@web ~]$ sudo cat /etc/ssh/sshd_config | grep Listen
ListenAddress 10.7.2.1
[nico@web ~]$ sudo systemctl restart sshd
nico@debian:~$ ssh nico@10.7.1.13
ssh: connect to host 10.7.1.13 port 22: Connection timed out
```
🌞 **Améliorer le niveau de sécurité du serveur**

- sur toutes les machines
- mettre en oeuvre au moins 3 configurations additionnelles pour améliorer le niveau de sécurité
- 3 lignes (au moins) à changer quoi
- le doc est vieux, mais en dehors des recommendations pour le chiffrement qui sont obsolètes, le reste reste très cool : [l'ANSSI avait édité des recommendations pour une conf OpenSSH](https://cyber.gouv.fr/publications/openssh-secure-use-recommendations)

# III. HTTP

## 1. Initial setup

🌞 **Monter un bête serveur HTTP sur `web.tp7.secu`**

- avec NGINX
- une page d'accueil HTML avec écrit "toto" ça ira
- **il ne doit écouter que sur l'IP du VPN**
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.1.1.1:80;

    # vous collez un ptit index.html dans ce dossier et zou !
    root /var/www/site_nul;
}
```

🌞 **Site web joignable qu'au sein du réseau VPN**

- le site web ne doit écouter que sur l'IP du réseau VPN
- le trafic à destination du port 80 n'est autorisé que si la requête vient du réseau VPN (firewall)
- prouvez qu'il n'est pas possible de joindre le site sur son IP host-only

🌞 **Accéder au site web**

- depuis votre PC, avec un `curl`
- vous êtes normalement obligés d'être co au VPN pour accéder au site

## 2. Génération de certificat et HTTPS

### A. Préparation de la CA

On va commencer par générer la clé et le certificat de notre Autorité de Certification (CA). Une fois fait, on pourra s'en servir pour signer d'autres certificats, comme celui de notre serveur web.

Pour que la connexion soit trusted, il suffira alors d'ajouter le certificat de notre CA au magasin de certificats de votre navigateur sur votre PC.

🌞 **Générer une clé et un certificat de CA**

```bash
# mettez des infos dans le prompt, peu importe si c'est fake
# on va vous demander un mot de passe pour chiffrer la clé aussi
$ openssl genrsa -des3 -out CA.key 4096
$ openssl req -x509 -new -nodes -key CA.key -sha256 -days 1024  -out CA.pem
$ ls
# le pem c'est le certificat (clé publique)
# le key c'est la clé privée
```

### B. Génération du certificat pour le serveur web

Il est temps de générer une clé et un certificat que notre serveur web pourra utiliser afin de proposer une connexion HTTPS.

🌞 **Générer une clé et une demande de signature de certificat pour notre serveur web**

```bash
$ openssl req -new -nodes -out web.tp7.secu.csr -newkey rsa:4096 -keyout web.tp7.secu.key
$ ls
# web.tp7.secu.csr c'est la demande de signature
# web.tp7.secu.key c'est la clé qu'utilisera le serveur web
```

🌞 **Faire signer notre certificat par la clé de la CA**

- préparez un fichier `v3.ext` qui contient :

```ext
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = web.tp7.secu
DNS.2 = www.tp7.secu
```

- effectuer la demande de signature pour récup un certificat signé par votre CA :

```bash
$ openssl x509 -req -in web.tp7.secu.csr -CA CA.pem -CAkey CA.key -CAcreateserial -out web.tp7.secu.crt -days 500 -sha256 -extfile v3.ext
$ ls
# web.tp7.secu.crt c'est le certificat qu'utilisera le serveur web
```

### C. Bonnes pratiques RedHat


🌞 **Déplacer les clés et les certificats dans l'emplacement réservé**

- gérez correctement les permissions de ces fichiers

### D. Config serveur Web

🌞 **Ajustez la configuration NGINX**

- le site web doit être disponible en HTTPS en utilisant votre clé et votre certificat
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.7.1.103:443 ssl;

    ssl_certificate /etc/pki/tls/certs/web.tp7.secu.crt;
    ssl_certificate_key /etc/pki/tls/private/web.tp7.secu.key;
    
    root /var/www/site_nul;
}
```

🌞 **Prouvez avec un `curl` que vous accédez au site web**

- depuis votre PC
- avec un `curl -k` car il ne reconnaît pas le certificat là

🌞 **Ajouter le certificat de la CA dans votre navigateur**

- vous pourrez ensuite visitez `https://web.tp7.b2` sans alerte de sécurité, et avec un cadenas vert
- il faut aussi ajouter l'IP de la machine à votre fichier `hosts` pour qu'elle corresponde au nom `web.tp7.b2`

> *En entreprise, c'est comme ça qu'on fait pour qu'un certificat de CA non-public soit trusted par tout le monde : on dépose le certificat de CA dans le navigateur (et l'OS) de tous les PCs. Evidemment, on utilise une technique de déploiement automatisé aussi dans la vraie vie, on l'ajoute pas à la main partout hehe.*

### E. Bonus renforcement TLS

⭐ **Bonus : renforcer la conf TLS**

- faites quelques recherches pour forcer votre serveur à n'utiliser que des méthodes de chiffrement fortes
- ça implique de refuser les connexions SSL, ou TLS 1.0, on essaie de forcer TLS 1.3

![Do you even](img/do_you_even.jpg)