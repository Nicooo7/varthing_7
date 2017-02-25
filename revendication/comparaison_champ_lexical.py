# coding: utf-8
import bs4
import re
import urllib.request
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup


app_name = 'revendication'

os.chdir("/Users/nicolasvinurel/Desktop/test")


class Champ_lexical:

	dictionnaire = {}

	def mettre_fichier_a_zero ():
		open ('vocabulaire', 'w')	

	def lister_mots_langue_francaise():
		with open("mots_langue_francaise",'w') as fichier:
			url = "http://www.pallier.org/ressources/dicofr/liste.de.mots.francais.frgut.txt"
			with urllib.request.urlopen(url) as f:
				data = f.read().decode('utf-8')


	def creer_le_dictionnaire ():

		def ajouter_au_dictionnaire (mot_cle):
					base = "http://www.rimessolides.com/motscles.aspx?m="
					url = """ {base}{mot_cle}""".format(base =base, mot_cle = mot_cle)
					with urllib.request.urlopen(url) as f:
						data = f.read().decode('utf-8')
						soup = bs4.BeautifulSoup(data, 'html.parser')
					for d in soup.find_all('a'):
						mot= d.get_text() 
						champ_lexical.append(mot) 
					for i in range (1,12):
						del champ_lexical[0]
					champ_lexical.reverse()
					for i in range (1,5):
						del champ_lexical[0]	
					champ_lexical.reverse()





		ajouter_au_dictionnaire (mot)

	


	def ecrire_le_dictionnaire(Champ_lexical.dictionnaire):
		dictionnaire = champ_lexical.dictionnaire 
		with open('vocabulaire', 'ab') as fichier:
			mon_pickler = pickle.Pickler(fichier)
			mon_pickler.dump(dictionnaire)


	def acceder_aux_vocabulaires():
	with open('vocabulaire', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		print (mon_depickler)
		un_mot = mon_depickler.load()
		while un_mot:
			un_mot = mon_depickler.load()
			print (un_mot.motcle)
			if un_mot.motcle == "fin":
				break


	




class Revendication:

	#------------------------definition------------------:	
	def __init__ (self, ennonce):
		
		self.ennonce = ennonce
		self.ennonce_filtre = []
		self.liste_des_termes_lies = []
		self.enumeration_vocabulaire = ""
		



	#--------------------------Methodes----------------------:
	def filtrer(self):
		ennonce = self.ennonce
		from nltk.tokenize import TreebankWordTokenizer
		from nltk.corpus import stopwords
		# On instancie notre tokenizer
		tokenizer = TreebankWordTokenizer()
		tokens = tokenizer.tokenize(ennonce)
		# chargement des stopwords français
		french_stopwords = set(stopwords.words('french'))
		# un petit filtre
		tokens = [token for token in tokens if token.lower() not in french_stopwords]	
		filtrat = []
		for element in tokens:
			self.ennonce_filtre.append(element) 
		print ("l'ennonce filtre est : {}".format (self.ennonce_filtre))


	def lister_les_termes_lies(self):
		champ_lexical =[]
		liste_mots_cle = self.ennonce_filtre
		for mot_cle in liste_mots_cle:
			base = "http://www.rimessolides.com/motscles.aspx?m="
			url = """ {base}{mot_cle}""".format(base =base, mot_cle = mot_cle)
			with urllib.request.urlopen(url) as f:
				data = f.read().decode('utf-8')
				soup = bs4.BeautifulSoup(data, 'html.parser')
			for d in soup.find_all('a'):
				mot= d.get_text() 
				champ_lexical.append(mot) 
			for i in range (1,12):
				del champ_lexical[0]
			champ_lexical.reverse()
			for i in range (1,5):
				del champ_lexical[0]	
			champ_lexical.reverse()
		self.liste_des_termes_lies = champ_lexical
		print ("la liste des termes lies  est : {}".format (self.lister_les_termes_lies))

		
		

	def enumeration(self):
		liste_vocabulaire = self.liste_des_termes_lies
		liste = ""
		for mot in liste_vocabulaire:
			liste = liste + " " + mot
		self.enumeration_vocabulaire = liste
		print ("l enumeration  est : {}".format (self.enumeration_vocabulaire))

 	#representations
	def __repr__ (self):
		return (self.ennonce)	


	#--------------------fonctions---------------------------:	

	#retourner le vocabulaire commun entre deux revendications
	def vocabulaire_commun(revendication1, revendication2):
		liste_vocabulaire1 = revendication1.liste_des_termes_lies
		liste_vocabulaire2 = revendication2.liste_des_termes_lies
		liste_commune = []

		for element in liste_vocabulaire1:
			if element in liste_vocabulaire2:
				liste_commune.append(element)
		print ("la liste commune est : {}".format(liste_commune))
		return liste_commune

	#retourner la proximite entre deux revendications		
	def proximite (revendication1, revendication2):
		liste_finale = Revendication.vocabulaire_commun(revendication1, revendication2)
		nb_element_retenus = len(liste_finale)
		nb_element_liste1 = len(revendication1.liste_des_termes_lies)
		nb_element_liste2 = len(revendication2.liste_des_termes_lies)
		nb_element_total = nb_element_liste1 + nb_element_liste2
		proximite = nb_element_retenus/ nb_element_total
		print ("la proximite est : {}".format(proximite))
		return proximite


def comparer_deux_revendications(ennonce1, ennonce2):

		revendication1 = Revendication (ennonce1)
		revendication1.filtrer()
		revendication1.lister_les_termes_lies()
		revendication1.enumeration()



		revendication2 = Revendication (ennonce2)
		revendication2.filtrer()
		revendication2.lister_les_termes_lies()
		revendication2.enumeration()

		Revendication.proximite(revendication1, revendication2)


def __main__ ():

	ennonce1 = "attraper les chiens errants et les tuer"
	ennonce2 = "sauver les baleines en Amazonie"



	comparer_deux_revendications (ennonce1, ennonce2)	
	
		


__main__ ()




















