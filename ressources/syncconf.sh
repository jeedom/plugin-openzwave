#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal
echo "Lancement de la synchronisation des configurations"
echo "Changement du répertoire courant"
cd /tmp
echo "Récupération du projet (cette étape peut durer quelques minutes)"
rm -rf /tmp/plugin-openzwave > /dev/null 2>&1
sudo git clone --depth=1 https://github.com/jeedom/plugin-openzwave.git 
if [ $? -ne 0 ]; then
    echo "Unable to fetch Jeedom git.Please check your internet connexion and github access"
    exit 1
fi
echo "Suppression des configurations Jeedom existantes"
sudo rm -fr /usr/share/nginx/www/jeedom/plugins/openzwave/core/config/devices/*
echo "Recopie des nouvelles configurations Jeedom"
cd plugin-openzwave/core/config/devices
sudo mv * /usr/share/nginx/www/jeedom/plugins/openzwave/core/config/devices/
echo "Suppression des configurations Openzwave existantes"
sudo rm -fr /usr/share/nginx/www/jeedom/plugins/openzwave/ressources/openzwave/config/*
echo "Recopie des nouvelles configurations Openzwave"
cd /tmp/plugin-openzwave/ressources/openzwave/config
sudo mv * /usr/share/nginx/www/jeedom/plugins/openzwave/ressources/openzwave/config/
echo "Nettoyage du répertoire temporaire"
sudo rm -R /tmp/plugin-openzwave
echo "Vos configurations sont maintenant à jour !"
