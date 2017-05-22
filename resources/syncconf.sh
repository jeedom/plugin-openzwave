#!/bin/bash

# This file is part of Plugin openzwave for jeedom.
#
#  Plugin openzwave for jeedom is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Plugin openzwave for jeedom is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Plugin openzwave for jeedom. If not, see <http://www.gnu.org/licenses/>.


logger_write(){
    NOW=$(date +"%Y-%m-%d %T")
    echo "[$NOW][$1] : $2"
}

logger_write "INFO" "Lancement de la synchronisation des configurations"
logger_write "INFO" "Déplacement dans le répertoire de travail"
cd /tmp
logger_write "INFO" "Nettoyage du répertoire de travail"
sudo rm -rf /tmp/plugin-openzwave > /dev/null 2>&1
sudo rm -rf /tmp/open-zwave > /dev/null 2>&1
logger_write "INFO" "Récupération des sources (cette étape peut durer quelques minutes)"
sudo git clone --depth=1 https://github.com/jeedom/plugin-openzwave.git
if [ $? -ne 0 ]; then
    logger_write "ERROR" "Unable to fetch Plugin-openzwave git. Please check your internet connexion and github access"
    exit 1
fi
sudo git clone --depth=1 https://github.com/OpenZWave/open-zwave.git
if [ $? -ne 0 ]; then
    ogger_write "ERROR" "Unable to fetch OpenZWave git. Please check your internet connexion and github access"
    exit 1
fi

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
logger_write "INFO" "Suppression des configurations Jeedom existantes"
sudo rm -rf ${BASEDIR}/../core/config/devices/*

logger_write "INFO" "Copie des nouvelles configurations Jeedom"
cd /tmp/plugin-openzwave/core/config/devices
sudo mv * ${BASEDIR}/../core/config/devices/

logger_write "INFO" "Suppression des configurations Openzwave existantes"
sudo rm -rf ${BASEDIR}/../resources/openzwaved/config/*

logger_write "INFO" "Copie des nouvelles configurations Openzwave"
cd /tmp/open-zwave/config
if [ ! -d  ${BASEDIR}/../resources/openzwaved/config ]; then
    mkdir -p ${BASEDIR}/../resources/openzwaved/config
fi
sudo mv * ${BASEDIR}/../resources/openzwaved/config/

logger_write "INFO" "Nettoyage du répertoire de travail"
sudo rm -R /tmp/plugin-openzwave
sudo rm -R /tmp/open-zwave
sudo chown -R www-data:www-data ${BASEDIR}/../resources/openzwaved/config/
sudo chown -R www-data:www-data ${BASEDIR}/../core/config/devices/

logger_write "INFO" "Vos configurations sont maintenant à jour !"
