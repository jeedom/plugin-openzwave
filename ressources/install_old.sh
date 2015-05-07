echo "********************************************************"
echo "*             Installation des dépendances             *"
echo "********************************************************"
sudo apt-get update  -y -q
sudo apt-get install -y mercurial subversion python-pip python-dev
sudo pip install cython==0.14
sudo apt-get install -y python-setuptools python-louie
sudo apt-get install -y python-sphinx make
sudo pip install sphinxcontrib-blockdiag sphinxcontrib-actdiag
sudo pip install sphinxcontrib-nwdiag sphinxcontrib-seqdiag
sudo apt-get install -y build-essential libudev-dev g++ gcc
sudo pip install urwid louie
sudo pip install flask flask-restful
echo "********************************************************"
echo "*             Installation de openZwave                *"
echo "********************************************************"
sudo mkdir /opt
sudo hg clone https://code.google.com/p/python-openzwave/ /opt/python-openzwave
cd /opt/python-openzwave
sudo ./update.sh
sudo ./compile.sh clean
sudo ./install.sh
sudo chmod 775 -R /opt/python-openzwave
sudo chown -R www-data:www-data /opt/python-openzwave
echo "********************************************************"
echo "*             Installation terminée                    *"
echo "********************************************************"