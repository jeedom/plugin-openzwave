#!/bin/bash
# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

set -x  # make sure each command is printed in the terminal


cd /opt/python-openzwave
sudo ./uninstall.sh
sudo rm -f zwcfg_*
sudo rm -Rf openzwave
sudo ./update.sh
sudo wget -O /opt/python-openzwave/openzwave/config/BeNext/SceneController.xml https://www.dropbox.com/s/qeb5kcks8u6qx29/SceneController.xml?dl=0
sudo wget -O /opt/python-openzwave/openzwave/cpp/src/command_classes/CentralScene.cpp https://www.dropbox.com/s/qdl1tlpzrrk9hzo/CentralScene.cpp?dl=0
sudo wget -O /opt/python-openzwave/openzwave/cpp/src/command_classes/CentralScene.h https://www.dropbox.com/s/zq6nlca903h8ye6/CentralScene.h?dl=0
sudo wget -O /opt/python-openzwave/CentralScene.diff https://www.dropbox.com/s/bafw4fz37xsgj9d/CentralScene-3.diff?dl=0
cd /opt/python-openzwave/openzwave
sudo patch -p0 -i ../CentralScene.diff
cd /opt/python-openzwave
sudo ./compile.sh clean
sudo ./install.sh
sudo chmod 775 -R /opt/python-openzwave
sudo chown -R www-data:www-data /opt/python-openzwave

echo "Everything is successfully installed!"