# coding: utf-8
import bs4
import re
import urllib.request
import pickle
import os

os.chdir("/Users/nicolasvinurel/Desktop/test")

with open('donnees', 'wb') as fichier:
	mon_pickler = pickle.Pickler(fichier)
 
actor_url = 'http://www.rimessolides.com/motscles.aspx?m=neige'
 
with urllib.request.urlopen(actor_url) as f:
    data = f.read().decode('utf-8')
    soup = bs4.BeautifulSoup(data, 'html.parser')

liste_de_mot =[]
for d in soup.find_all('a'):
	mot= d.get_text() 
	liste_de_mot.append(mot) 
  
print (liste_de_mot)
mon_pickler.dump(liste_de_mot)	

	

