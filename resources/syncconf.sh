#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal
NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Lancement de la synchronisation des configurations"
echo "[$NOW][INFO] : Déplacement dans le répertoire de travail"
cd /tmp
echo "[$NOW][INFO] : Nettoyage du répertoire de travail"
sudo rm -rf /tmp/plugin-openzwave > /dev/null 2>&1
sudo rm -rf /tmp/open-zwave > /dev/null 2>&1
echo "[$NOW][INFO] : Récupération des sources (cette étape peut durer quelques minutes)"
sudo git clone --depth=1 https://github.com/jeedom/plugin-openzwave.git
if [ $? -ne 0 ]; then
    NOW=$(date +"%Y-%m-%d %T")
    echo "[$NOW][ERROR] : Unable to fetch Jeedom git. Please check your internet connexion and github access"
    exit 1
fi
sudo git clone --depth=1 https://github.com/OpenZWave/open-zwave.git
if [ $? -ne 0 ]; then
    NOW=$(date +"%Y-%m-%d %T")
    echo "[$NOW][ERROR] : Unable to fetch OpenZWave git. Please check your internet connexion and github access"
    exit 1
fi

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Suppression des configurations Jeedom existantes"
sudo rm -rf ${BASEDIR}/../core/config/devices/*

NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Copie des nouvelles configurations Jeedom"
cd /tmp/plugin-openzwave/core/config/devices
sudo mv * ${BASEDIR}/../core/config/devices/

NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Suppression des configurations Openzwave existantes"
sudo rm -rf ${BASEDIR}/../resources/openzwaved/config/*

NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Copie des nouvelles configurations Openzwave"
cd /tmp/open-zwave/config
if [ ! -d  ${BASEDIR}/../resources/openzwaved/config ]; then
    mkdir -p ${BASEDIR}/../resources/openzwaved/config
fi
sudo mv * ${BASEDIR}/../resources/openzwaved/config/

NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Nettoyage du répertoire de travail"
sudo rm -R /tmp/plugin-openzwave
sudo rm -R /tmp/open-zwave
sudo chown -R www-data:www-data ${BASEDIR}/../resources/openzwaved/config/
sudo chown -R www-data:www-data ${BASEDIR}/../core/config/devices/

NOW=$(date +"%Y-%m-%d %T")
echo "[$NOW][INFO] : Vos configurations sont maintenant à jour !"
