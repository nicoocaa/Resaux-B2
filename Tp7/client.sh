#!/bin/bash


# Vérifie si WireGuard est installé
if command -v wg >/dev/null 2>&1; then
    echo "Tout les prérequis sont présent la configuration va commencer"
else
    echo "WireGuard n'est pas installé. Installez-le avec la commande :"
    echo "sudo dnf install wireguard-tools"
    exit 1
fi

echo "Quelles est l'ip que vous voulez atribuer au client"
echo "Format de l'ip 10.10.10.10/24 requis"
read ip 

cd 

mkdir wireguard
cd wireguard

wg genkey | tee john.key | wg pubkey > john.pub

private_key=$(cat john.key)
public_key=$(cat john.pub)



cat > "john.conf" <<EOF
[Interface]
Address = $ip
PrivateKey = $private_key

[Peer]
PublicKey = 6cJJPNLgVUILIRJrA0bfGw8j9pvRix7bcjmV9uTCtlE=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
EOF

# Affichage des informations pour le serveur
echo "---------------------------------------------------------------------------------------------"
echo "Veuillez ajouter les lignes suivantes au fichier de configuration de votre serveur VPN (/etc/wireguard/wg0.conf) :"
echo
cat <<EOF

[Peer]
PublicKey = $public_key
AllowedIPs = $ip
EOF
echo "---------------------------------------------------------------------------------------------"

# Ajout des alias pour la connexion/déconnexion
echo "alias vpn-C='sudo wg-quick up $PWD/john.conf && sudo ip route add default dev wg0'" >> ~/.bashrc
echo "alias vpn-D='sudo wg-quick down $PWD/john.conf && sudo ip route del default dev wg0'" >> ~/.bashrc

# Recharger le fichier ~/.bashrc pour que les alias soient pris en compte immédiatement
source ~/.bashrc

echo " Aprés avoir édité le fichier de conf de votre vpn vous pouver lancer les commandes suivante "
echo "vpn-C  pour vous connecter au vpn "
echo "vpn-D pour vous déconecter du vpn "

