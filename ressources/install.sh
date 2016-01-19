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
PYTHON_OPENZWAVE_VERSION=9ed302eec778d1c6bb3395a368e34fc33a01cce3 # 0.3.0b8
OPENZWAVE_VERSION=1c2511bb46d935864f0a6ff19fd804028b7beab3 # 1.4.8

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
apt_install mercurial git python-pip python-dev python-setuptools python-louie python-sphinx make build-essential libudev-dev g++ gcc python-lxml unzip libjpeg-dev
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
sudo sed -i '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
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
fi

if [ $(grep 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200"' /etc/udev/rules.d/98-usb-serial.rules | wc -l) -eq 0 ]; then
  if [ -f /etc/udev/rules.d/98-usb-serial.rules ]; then
    sudo cp /etc/udev/rules.d/98-usb-serial.rules /tmp/udev
  else
    touch /tmp/udev
  fi
  sudo echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="ttyUSB21"' >> /tmp/udev
  sudo mv /tmp/udev /etc/udev/rules.d/98-usb-serial.rules
fi
echo 100 > /tmp/compilation_ozw_in_progress
echo "Everything is successfully installed!"
rm /tmp/compilation_ozw_in_progress

