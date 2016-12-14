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

class Vocabulaire: #motclé et  son champs lexical.
	
	def __init__(self,motcle):
		base = "http://www.rimessolides.com/motscles.aspx?m="
		url = """ {base}{motcle}""".format(base =base, motcle = motcle)
		with urllib.request.urlopen(url) as f:
		    data = f.read().decode('utf-8')
		    soup = bs4.BeautifulSoup(data, 'html.parser')

		champ_lexical =[]
		for d in soup.find_all('a'):
			mot= d.get_text() 
			champ_lexical.append(mot) 
		for i in range (1,12):
			del champ_lexical[0]
		champ_lexical.reverse()
		for i in range (1,5):
			del champ_lexical[0]	
		champ_lexical.reverse()


		self.motcle = motcle
		self.champ_lexical = champ_lexical

	
def afficher_bonjour():
	print ("bonjour")


def initialiser_le_fichier():
	with open('vocabulaire', 'wb') as fichier:
		mon_pickler = pickle.Pickler(fichier)
		le_mot = Vocabulaire("debut")
		mon_pickler.dump(le_mot)

def enregistrer_un_nouveau_mot(mot):
	with open('vocabulaire', 'ab') as fichier:
		liste_des_vocabulaires = []
		le_mot = Vocabulaire(mot)
		mon_pickler = pickle.Pickler(fichier)
		mon_pickler.dump(le_mot)

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

def implementer_la_liste_des_vocabulaires(la_liste_des_vocabulaires):

	with open('vocabulaire', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		un_mot = mon_depickler.load()
		while un_mot:
			un_mot = mon_depickler.load()
			if un_mot.motcle == "fin":
				break
			else:
				une_liste = []
				une_liste.append(un_mot.motcle)
				for element in un_mot.champ_lexical:
					une_liste.append(element)
				la_liste_des_vocabulaires.append(une_liste)
				print



def filtrer_ennonce(ennonce,filtrat):
	from nltk.tokenize import TreebankWordTokenizer
	from nltk.corpus import stopwords
	# On instancie notre tokenizer
	tokenizer = TreebankWordTokenizer()

	tokens = tokenizer.tokenize(ennonce)

	# chargement des stopwords français
	french_stopwords = set(stopwords.words('french'))

	# un petit filtre
	tokens = [token for token in tokens if token.lower() not in french_stopwords]
	filtrat2 = []
	for element in tokens:
		filtrat2.append(element)
		print ("voici les mots obtenus: {0}".format(filtrat2))

	for element in filtrat2:
		elementx = element
		print (elementx)
		def essayer_d_alimenter_le_filtrat(elementx):
			base = "http://www.linternaute.com/dictionnaire/fr/definition/"
			url = """ {base}{motcle}""".format(base =base, motcle = elementx)
			print (url)
			with urllib.request.urlopen(url) as f:
				data = f.read().decode('utf-8')
				soup = bs4.BeautifulSoup(data, 'html.parser')
				#on récupère dans la page la catégorie grammaticale du mot
				print ("*******************")
				for section in soup.find_all("span",class_="dico_title_definition"):
					categorie = section.get_text() 
					#on teste s'il s'agit d'un nom
					num = categorie.find("nom")
					print ("l'élément {0} est un {1}".format (element, categorie))
					print (num)
					if num != -1:
						#on enregistre l'élément dans la liste filtrat 
						filtrat.append(element)
					if re.match(r"A-Z", element) != "none":
						print ("ca match")
						filtrat.append(element)

		try:
			essayer_d_alimenter_le_filtrat(elementx)
			stop = "ok"
			print (stop)	
		except:
			if stop != "ok":
				try:
					element2 = element[:-1]
					print (element2)
					essayer_d_alimenter_le_filtrat(element2)
					stop = "ok"
				except:
					if stop != "ok":
						print ("temps pis")	

	print (filtrat)
			




def champ_lexical_des_propositions():
	#pour chaque proposition
	#propositions = Proposition.objects.all()
	#for proposition in propositions:
	#récupérer l'ennoncé de la propostion
		#ennonce = proposition.ennonce
	print("bonjour")	



def liste_a_partir_d_un_ennonce (ennonce):	
	print ("LISTE A PARTIR D'UN ENNONCE ")	
	filtrat = []
	filtrer_ennonce(ennonce,filtrat)
	initialiser_le_fichier()
	for mot in filtrat:
		print ("*****************")
		print ("on va enregister le mot {0}".format (mot))
		enregistrer_un_nouveau_mot(mot)
	enregistrer_un_nouveau_mot("fin")

	la_liste_des_vocabulaires = []
	implementer_la_liste_des_vocabulaires (la_liste_des_vocabulaires)
		
	liste = ""
	for une_liste in la_liste_des_vocabulaires:
		for un_mot in une_liste:
				liste = liste + " " + un_mot
	print (liste)
	return (liste)
	#proposition.champ_lexical = liste
	#proposition.save()


def comparer_des_propositions (ennonce1, ennonce2):
	print ("COMPARER DES PROPOSITIONS")
	liste1= liste_a_partir_d_un_ennonce (ennonce1)
	print ("voici la liste1: {0}".format (liste1))
	liste2 = liste_a_partir_d_un_ennonce (ennonce2)
	



	def filtrer_une_liste(liste):
		print ("FILTRER UNE LISTE")
		from nltk.tokenize import TreebankWordTokenizer
		from nltk.corpus import stopwords
		# On instancie notre tokenizer
		tokenizer = TreebankWordTokenizer()
		tokens = tokenizer.tokenize(liste)
		# chargement des stopwords français
		french_stopwords = set(stopwords.words('french'))
		# un petit filtre
		tokens = [token for token in tokens if token.lower() not in french_stopwords]
		filtrat2 = []
		for element in tokens:
			filtrat2.append(element)
		print ("voici les mots obtenus: {0}".format(filtrat2))
		return (filtrat2)


	liste1 = filtrer_une_liste(liste1)
	liste2 = filtrer_une_liste(liste2)
	print (liste1)
	print ()
	print (liste2)
	print ("******************")



	def trouver_les_mots_communs_des_listes(liste1, liste2):
		print ("TROUVER LES MOTS COMMUNS DES LISTES")
		liste_finale = []
		for element in liste1:
			if element in liste2:
				print ("l'element{0} est dans les deux listes".format(element))
				liste_finale.append(element)
			#else: 
				#print ("l'element {0} n'est pas dans les deux listes".format (element))	
		return liste_finale


	liste_finale = trouver_les_mots_communs_des_listes(liste1,liste2)
	print ("la liste finale est : {0}".format (liste_finale))
	

	def supprimer_les_doublons(liste_finale) :
		liste_f = liste_finale
		for element in liste_f:
			print ("********************")
			print ("on considère le mot {0}".format (element))
			while liste_finale.count(element)>1:
				print ("le mot {0} apparait {1} fois".format (element, liste_finale.count(element)))
				liste_finale.remove(element)
				print ("on va supprimer le mot {0}".format(element))
		return (liste_finale)


	liste_finale = supprimer_les_doublons(liste_finale)
	
	print ("la liste commune est : {0}".format(liste_finale))
	
	def calculer_la_proximite ():
		nb_element_retenus = len(liste_finale)
		nb_element_liste1 = len(liste1)
		nb_element_liste2 = len(liste2)
		nb_element_total = nb_element_liste1 + nb_element_liste2

		proximite = nb_element_retenus/ nb_element_total

		print ("la proximité est de {0}".format(proximite))
	calculer_la_proximite()	



comparer_des_propositions ("faire un safari en Afrique du Sud ", "lutter contre le racisme")











































