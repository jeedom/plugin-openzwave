#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal
touch /tmp/compilation_ozw_in_progress
echo 0 > /tmp/compilation_ozw_in_progress
echo "Lancement de l'installation/mise à jour des dépendances openzwave"

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ARCH=`uname -m`
PYTHON_OPENZWAVE_VERSION=1ca17acabc64fe857f7c1ee412426af8defaaaf0 # 0.3.0
OPENZWAVE_VERSION=00eb2073057b24759e29a5ee2877939682661579 # 1.4.2088

function apt_install {
  sudo apt-get -y install "$@"
  if [ $? -ne 0 ]; then
    echo "could not install $1 - abort"
    rm /tmp/compilation_ozw_in_progress
    exit 1
  fi
}

function pip_install {
  sudo pip install "$@"
  if [ $? -ne 0 ]; then
    echo "could not install $p - abort"
    rm /tmp/compilation_ozw_in_progress
    exit 1
  fi
}

if [ $(ps ax | grep z-way-server | grep -v grep | wc -l ) -ne 0 ]; then
  echo "Désactivation du z-way-server"
  sudo service z-way-server stop
  sudo service mongoose stop
  sudo service zbw_connect stop
  sudo update-rc.d -f z-way-server remove
  sudo update-rc.d -f mongoose remove
  sudo update-rc.d -f zbw_connect remove
  ps aux | grep mongoose | awk '{print $2}' | xargs kill -9
  ps aux | grep z-way-server | awk '{print $2}' | xargs kill -9 
  ps aux | grep zbw_connect | awk '{print $2}' | xargs kill -9 
  sudo rm -rf /opt/z-way-server*
fi

if [ ! -d /opt ]; then
  sudo mkdir /opt
fi
echo 10 > /tmp/compilation_ozw_in_progress
sudo rm -f /var/lib/dpkg/updates/*
sudo apt-get clean
echo 20 > /tmp/compilation_ozw_in_progress
sudo apt-get update
echo 30 > /tmp/compilation_ozw_in_progress
echo "Installation des dependances"
apt_install mercurial git python-pip python-dev python-pyudev python-setuptools python-louie python-sphinx make build-essential libudev-dev g++ gcc python-lxml unzip libjpeg-dev python-serial python-requests
echo 40 > /tmp/compilation_ozw_in_progress
# Python
echo "Installation des dependances Python"
pip_install sphinxcontrib-blockdiag
echo 41 > /tmp/compilation_ozw_in_progress
pip_install sphinxcontrib-actdiag
echo 42 > /tmp/compilation_ozw_in_progress
pip_install sphinxcontrib-nwdiag
echo 43 > /tmp/compilation_ozw_in_progress
pip_install sphinxcontrib-seqdiag
echo 44 > /tmp/compilation_ozw_in_progress
pip_install urwid
echo 45 > /tmp/compilation_ozw_in_progress
pip_install louie
echo 46 > /tmp/compilation_ozw_in_progress
pip_install flask
echo 47 > /tmp/compilation_ozw_in_progress
pip_install flask-restful
echo 48 > /tmp/compilation_ozw_in_progress
pip_install flask-httpauth
echo 49 > /tmp/compilation_ozw_in_progress
pip_install six
echo 50 > /tmp/compilation_ozw_in_progress

sudo mkdir /opt
if [ -d /opt/python-openzwave ]; then
  cd /opt/python-openzwave
  echo "Désinstallation de la version précédente";
  sudo make uninstall > /dev/null 2>&1
  echo 55 > /tmp/compilation_ozw_in_progress
  sudo rm -fr /usr/local/lib/python2.7/dist-packages/libopenzwave*
  sudo rm -fr /usr/local/lib/python2.7/dist-packages/openzwave* 
  cd /opt
  sudo rm -fr /opt/python-openzwave
fi
# Installation de Python-OpenZwave
echo "Installation de Python-OpenZwave"
cd /opt
sudo git clone https://github.com/OpenZWave/python-openzwave.git
if [ $? -ne 0 ]; then
  echo "Unable to fetch OpenZWave git.Please check your internet connexion and github access"
  rm /tmp/compilation_ozw_in_progress
  exit 1
fi
echo 60 > /tmp/compilation_ozw_in_progress
cd python-openzwave
sudo git reset --hard ${PYTHON_OPENZWAVE_VERSION}
sudo pip uninstall -y Cython
cd /opt/python-openzwave
sudo make cython-deps
echo 65 > /tmp/compilation_ozw_in_progress
sudo make repo-deps
echo 70 > /tmp/compilation_ozw_in_progress
sudo git clone https://github.com/OpenZWave/open-zwave.git openzwave
if [ $? -ne 0 ]; then
  echo "Unable to fetch OpenZWave git.Please check your internet connexion and github access"
  rm /tmp/compilation_ozw_in_progress
  exit 1
fi
echo 75 > /tmp/compilation_ozw_in_progress
cd openzwave
sudo git reset --hard ${OPENZWAVE_VERSION}
cd /opt/python-openzwave
# sudo sed -i '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
sudo make install-api
echo 80 > /tmp/compilation_ozw_in_progress
sudo mkdir /opt/python-openzwave/python-eggs
sudo chown -R www-data:www-data /opt/python-openzwave
sudo chmod -R 777 /opt/python-openzwave
echo 90 > /tmp/compilation_ozw_in_progress
if [ -e /dev/ttyAMA0 ];  then 
  sudo sed -i 's/console=ttyAMA0,115200//; s/kgdboc=ttyAMA0,115200//' /boot/cmdline.txt
  sudo sed -i 's|[^:]*:[^:]*:respawn:/sbin/getty[^:]*ttyAMA0[^:]*||' /etc/inittab
fi

if [ -e /dev/ttymxc0 ];  then 
  sudo systemctl mask serial-getty@ttymxc0.service
  sudo systemctl stop serial-getty@ttymxc0.service
fi
if [ -e /dev/ttyAMA0 ];  then 
  sudo systemctl mask serial-getty@ttyAMA0.service
  sudo systemctl stop serial-getty@ttyAMA0.service
fi
# Disable bluetooth Raspberry Pi 3 if use a Razberry board
RPI_BOARD_REVISION=`grep Revision /proc/cpuinfo | cut -d: -f2 | tr -d " "`
if [[ $RPI_BOARD_REVISION ==  "a02082" || $RPI_BOARD_REVISION == "a22082" ]]
then
   systemctl disable hciuart
   # Add "dtoverlay=pi3-miniuart-bt" to /boot/config.txt if needed
   if [[ ! `grep "dtoverlay=pi3-miniuart-bt" /boot/config.txt` ]]
   then
      echo "Raspberry Pi 3 Detected. If you use a Razberry board you must Disabling Bluetooth"
      echo "Please add 'dtoverlay=pi3-miniuart-bt' to the end of the file /boot/config.txt"
      #echo "dtoverlay=pi3-miniuart-bt" >> /boot/config.txt
      # stop BT modem trying to use UART
      #sudo systemctl disable hciuart
      echo "And reboot your Raspberry Pi"
   fi
fi
echo 100 > /tmp/compilation_ozw_in_progress
echo "Everything is successfully installed!"
rm /tmp/compilation_ozw_in_progress

