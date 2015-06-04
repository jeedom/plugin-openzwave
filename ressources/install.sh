#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal

function apt_install {
  sudo apt-get -y install $1
  if [ $? -ne 0 ]; then
    echo "could not install $1 - abort"
    exit 1
  fi
}

function pip_install {
  sudo pip install "$@"
  if [ $? -ne 0 ]; then
    echo "could not install $p - abort"
    exit 1
  fi
}

sudo apt-get update --fix-missing


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
  if [ -e /dev/ttymxc0 ]; then
     sudo systemctl unmask serial-getty@ttymxc0.service
  fi
  sudo rm -rf /opt/z-way-server*
fi

# Minimal installation for a Python ecosystem
# for OpenZwave

# Dpkg
echo "Installation des dependances"
apt_install mercurial
apt_install git
apt_install python-pip
apt_install python-dev
apt_install python-setuptools
apt_install python-louie
apt_install python-sphinx
apt_install make
apt_install build-essential
apt_install libudev-dev
apt_install g++
apt_install gcc


# Python
echo "Installation des dependances Python"
pip_install cython==0.14
pip_install sphinxcontrib-blockdiag
pip_install sphinxcontrib-actdiag
pip_install sphinxcontrib-nwdiag
pip_install sphinxcontrib-seqdiag
pip_install urwid
pip_install louie
pip_install flask
pip_install flask-restful

# Installation de Python-OpenZwave
echo "Installation de Python-OpenZwave"
sudo mkdir /opt

if [ ! -d /opt/python-openzwave/.git ]; then
    echo "Download sources of Python-Openzwave";
    if [ -d /opt/python-openzwave ]; then
    	sudo rm -Rf /opt/python-openzwave;
    fi
    sudo git clone https://github.com/jeedom/python-openzwave.git --depth=1 --quiet /opt/python-openzwave;
    if [ $1 = 'dev' ]; then
      cd /opt/python-openzwave;
      sudo git checkout dev;
    fi
    cd /opt/python-openzwave;
else 
	echo "Update sources of python-openzwave";
	cd /opt/python-openzwave;
  sudo git remote set-url origin https://github.com/jeedom/python-openzwave.git;
	sudo git fetch --all
	sudo git reset --hard origin/master
  if [ $1 = 'dev' ]; then
     sudo git checkout dev;
  fi
	sudo git pull;
fi

if [ ! -d openzwave/.git ]; then
    echo "Download sources of Openzwave";
    if [ -d openzwave ]; then
    	sudo rm -Rf /opt/python-openzwave/openzwave;
    fi
    sudo git clone https://github.com/jeedom/open-zwave.git --depth=1 --quiet openzwave;
    if [ $1 = 'dev' ]; then
      cd openzwave;
      sudo git checkout dev;
      cd ..;
    fi
else 
	echo "Update sources of Openzwave";
	cd openzwave;
  sudo git remote set-url origin https://github.com/jeedom/open-zwave.git;
	sudo git fetch --all;
	sudo git reset --hard origin/master;
  if [ $1 = 'dev' ]; then
     sudo git checkout dev;
  fi
	sudo git pull;
fi
echo "Sources updated"
cd /opt/python-openzwave
#sudo make deps
#sudo make update
sudo make clean
sudo make build
sudo make install

#sudo /opt/python-openzwave/compile.sh clean
#sudo /opt/python-openzwave/install.sh
sudo mkdir /opt/python-openzwave/python-eggs
sudo chmod 775 -R /opt/python-openzwave
sudo chown -R www-data:www-data /opt/python-openzwave
sudo chmod 700 -R /opt/python-openzwave/python-eggs

if [ $(grep 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200"' /etc/udev/rules.d/98-usb-serial.rules | wc -l) -eq 0 ]; then
    if [ -f /etc/udev/rules.d/98-usb-serial.rules ]; then
      sudo cp /etc/udev/rules.d/98-usb-serial.rules /tmp/udev
    else
      touch /tmp/udev
    fi
    sudo echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="ttyUSB21"' >> /tmp/udev
    sudo mv /tmp/udev /etc/udev/rules.d/98-usb-serial.rules
fi

echo "Everything is successfully installed!"