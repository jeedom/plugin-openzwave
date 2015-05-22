#!/usr/bin/python
#sarakha63 for jeedom
from xml.dom import minidom
import os
import glob
import urllib

curdir=os.path.dirname(os.path.abspath(__file__))####repertoire courant
urllib.urlretrieve ("https://raw.githubusercontent.com/OpenZWave/open-zwave/master/config/manufacturer_specific.xml", "manuf.xml")#recuperation du fichier ozw
rootdir=os.path.dirname(os.path.dirname(curdir))##rep paretn deux fois
jeeconfrep=os.path.join(rootdir,'core\\config\\devices')####rep conf jeedom
jeeimgrep=os.path.join(rootdir,'core\\img\\devices')####rep image jeedom
outfile=os.path.join(curdir, 'out_ozw.csv')##definition du fichier 1
outnoozw=os.path.join(curdir, 'no_ozw.csv')##definition du fichier 2
for file in [outfile,outnoozw]:##suppression des fichiers si ils existent
	if os.path.exists(file):
		os.remove(file)
fichier = open(outfile,'a')###ouverture fichier en mode append
fichier.write('Marque;Produit;Manuf Id;Product Type;Productid;Conf Jeedom;Image Jeedom;Nom conf Jeedom;Fichier de conf OZW \n')######creation entete
xmldoc = minidom.parse(os.path.join(curdir,'manuf.xml'))####fichier de conf manuf specific ozw
itemlist = xmldoc.getElementsByTagName('Manufacturer')###on construit la liste des blocs manufacturer
exceptchars=['/','(',')','[',']']#####liste de caratere a eviter dans le nom de conf
listnormalnoconf=[]######liste des confs ou il est normal de pas avoir de parametres OZW
listproductOZW=[]#init liste product OZW servira dans la deuxieme analyse
###### PREMIERE PARTIE
######parcours du xml
for manuf in itemlist:###pour chaque marque
	manufname=manuf.attributes['name'].value####nom marque
	manufid=str(int(manuf.attributes['id'].value,16))####id marque
	for product in manuf.getElementsByTagName('Product'):#####pour chaque produit
		hasimg=''
		hasconf=''
		producttype=str(int(product.attributes['type'].value,16))###type produit
		productid=str(int(product.attributes['id'].value,16))####id produit
		productname=product.attributes['name'].value###nomproduit
		allid=manufid+'.'+producttype+'.'+productid+'_' #concatenation des ids
		try:###certains modules n ont pas de config ozw
			productconfig=product.attributes['config'].value###on cherche config
			listproductOZW.append(allid[:-1]) ##on rajoute les ids dasn la liste
		except:####si pas trouve
			productconfig='N/A'###on met na
		confname=(manufname+'.'+productname).lower().replace(' ','.')##concatenation marque produit en minuscule sans espace
		for char in exceptchars:####on parcourt la liste des caracteres
			confname=confname.replace(char,'')####on les supprime
		if len(glob.glob(os.path.join(jeeimgrep,allid+'*')))!=0:
			hasimg='X'
		if len(glob.glob(os.path.join(jeeconfrep,allid+'*.json')))!=0:
			hasconf='X'
		fichier.write(manufname + ';' +productname+';'+manufid+';' + producttype + ';' +productid+';'+hasconf+';'+hasimg+';'+allid+confname+';'+productconfig+'\n')##ecriture de la ligne
fichier.close()###on ferme le fichier
###### DEUXIEME PARTIE
####parcourt des confs exsitantes dans jeedom pour voir si elles existent dans ozw
actualjeeconf = [ f for f in os.listdir(jeeconfrep) if os.path.isfile(os.path.join(jeeconfrep,f)) ]###on construit la liste des confs jeedom
fichiernozow = open(outnoozw,'a')###on ouvre le fichier
for jeeconf in actualjeeconf: ###pour toutes les confs jeedom
	jeeconfid=jeeconf[:jeeconf.find('_')]##on recupere la partie id
	if jeeconfid not in listproductOZW:##si non presente dans la liste des confs OZW avec parametre et non presente dans la liste des normals sans confs
		fichiernozow.write(jeeconf+'\n')
fichiernozow.close()
