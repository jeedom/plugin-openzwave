#!/bin/bash

# Automatically generated script by
# vagrantbox/doc/src/vagrant/src-vagrant/deb2sh.py
# The script is based on packages listed in debpkg_minimal.txt.

#set -x  # make sure each command is printed in the terminal

cd /opt/python-openzwave/openzwave
sudo touch /tmp/updateConfOpenzwave
sudo git reset --hard HEAD
sudo git pull
sudo find config/ -newer /tmp/updateConfOpenzwave | grep xml >> /tmp/updatedConfOpenzwave
rm /tmp/updateConfOpenzwave