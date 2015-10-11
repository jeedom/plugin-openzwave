#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal
echo "Lancement de l'installation/mise à jour des dépendances openzwave"

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ARCH=`uname -m`
PYTHON_OPENZWAVE_VERSION=4f43a0bdb4c3c42c9edd4c887eeb77758663ab64
OPENZWAVE_VERSION=0a73afbe4114e8d6f0593b55f13a48130d095bb9

function apt_install {
  sudo apt-get -y install "$@"
  if [ $? -ne 0 ]; then
    sudo service jeedom start
    echo "could not install $1 - abort"
    exit 1
  fi
}

function pip_install {
  sudo pip install "$@"
  if [ $? -ne 0 ]; then
    sudo service jeedom start
    echo "could not install $p - abort"
    exit 1
  fi
}

sudo service jeedom stop

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

sudo rm -f /var/lib/dpkg/updates/*
sudo apt-get clean
sudo apt-get update

echo "Installation des dependances"
apt_install mercurial git python-pip python-dev python-setuptools python-louie python-sphinx make build-essential libudev-dev g++ gcc python-lxml unzip

# Python
echo "Installation des dependances Python"
pip_install sphinxcontrib-blockdiag
pip_install sphinxcontrib-actdiag
pip_install sphinxcontrib-nwdiag
pip_install sphinxcontrib-seqdiag
pip_install urwid
pip_install louie
pip_install flask
pip_install flask-restful

if [  -z "$1" -a $(uname -a | grep cubox | wc -l ) -eq 1 -a ${ARCH} = "armv7l" ]; then
  echo "Armv7/Jeedomboard installation direct"
  sudo cp /opt/python-openzwave/zwcfg* /opt
  sudo cp -r /opt/python-openzwave/xml_backups /opt
  sudo rm -fr /opt/python-openzwave
  sudo mkdir -p /opt/python-openzwave
  cp -R ${BASEDIR}/python-openzwave/armv7/*  /usr/local/lib/python2.*/dist-packages
  sudo cp /opt/zwcfg* /opt/python-openzwave
  sudo cp -r /opt/xml_backups /opt/python-openzwave
  sudo rm -fr /opt/xml_backups
  sudo rm -f /opt/zwcfg*
else
  sudo mkdir /opt
  if [ -d /opt/python-openzwave ]; then
    echo "Sauvegarde du fichier de conf";
    sudo cp /opt/python-openzwave/zwcfg* /opt
    sudo cp -r /opt/python-openzwave/xml_backups /opt
    cd /opt/python-openzwave
    echo "Désinstallation de la version précédente";
    sudo make uninstall > /dev/null 2>&1
    sudo rm -fr /usr/local/lib/python2.7/dist-packages/libopenzwave*
    sudo rm -fr /usr/local/lib/python2.7/dist-packages/python_openzwave_*
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
    exit 1
  fi
  cd python-openzwave
  sudo git reset --hard ${PYTHON_OPENZWAVE_VERSION}
  sudo pip uninstall -y Cython
  cd /opt/python-openzwave
  sudo make cython-deps
  sudo make repo-deps
  sudo git clone https://github.com/OpenZWave/open-zwave.git openzwave
  if [ $? -ne 0 ]; then
    echo "Unable to fetch OpenZWave git.Please check your internet connexion and github access"
    exit 1
  fi
  cd openzwave
  sudo git reset --hard ${OPENZWAVE_VERSION}
  cd /opt/python-openzwave
  sudo sed -i '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
  sudo make install-api
  sudo mkdir /opt/python-openzwave/python-eggs
  sudo cp /opt/zwcfg* /opt/python-openzwave/.
  sudo cp -r /opt/xml_backups /opt/python-openzwave
  sudo rm -fr /opt/xml_backups
  sudo rm -f /opt/zwcfg*
fi

sudo chown -R www-data:www-data /opt/python-openzwave
sudo chmod -R 777 /opt/python-openzwave

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
sudo service jeedom start
echo "Everything is successfully installed!"
