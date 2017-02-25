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
			del liste_de_mot[0]
		champ_lexical.reverse()
		for i in range (1,5):
			del champ_lexical[0]	
		champ_lexical.reverse()
		print (champ_lexical)


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



def filtrer_ennonce(ennonce):
	from nltk.tokenize import TreebankWordTokenizer
	from nltk.corpus import stopwords
	# On instancie notre tokenizer
	tokenizer = TreebankWordTokenizer()

	tokens = tokenizer.tokenize(ennonce)

	# chargement des stopwords français
	french_stopwords = set(stopwords.words('french'))

	# un petit filtre
	tokens = [token for token in tokens if token.lower() not in french_stopwords]


	print(tokens)  
	


def creer_les_proximites():
	

	#compter_les_utilisateurs:
	utilisateurs = User.objects.all()
	for utilisateur in utilisateurs:
		liste_des_tuples = []
		liste_des_probabilites = []
		liste_des_utilisateurs = []
		utilisateurs = User.objects.all().exclude(id = utilisateur.id)
		i=0
		for element in utilisateurs:
			i= i+1
		nombre_utilisateur = i
		print ("nombre d'utilisateur :{0}".format(i))
		print ("propositions soutenues par moi :{0}".format(Proposition.objects.filter(soutien__user = utilisateur)))
		#recupérer la première revendication que j'ai en commun avec un utilisateur
		
		for un_utilisateur in utilisateurs:
			print ("ON VA DETERMINER LES PROXIMITES DE {0} avec {1} ".format(utilisateur, un_utilisateur))
			mes_propositions = Proposition.objects.filter(soutien__user = utilisateur).filter(soutien__user = un_utilisateur)
			print ("propositions soutenues par l'autre :{0}".format(Proposition.objects.filter(soutien__user = un_utilisateur)))

			print ("les propositions communes :{0}".format(mes_propositions))


			#pour chaque proposition:
			probabilite = 1
			for proposition in mes_propositions:
				#compter le nombre de soutien de la proposition
				soutiens = User.objects.filter (soutien__propositions = proposition)
				i=0
				for element in soutiens:
					print ("soutien :{0}".format(element.username))
					i= i+1
				nombre_soutien_proposition = i
				print ("nombre de soutien de la première proposition :{0}".format(i))
			#probabilité qu'un utilisateur lambda adhère à mes propositions
				proba = nombre_soutien_proposition/nombre_utilisateur
				probabilite = probabilite * proba
				print ("probabilité en cours de calcul :{0}".format(probabilite))
			print ("probabilité en cours de calcul concernant l'utilisateur {0} :{1}".format(un_utilisateur, probabilite))
			a = (un_utilisateur, probabilite)
			u = un_utilisateur
			p= probabilite
			liste_des_utilisateurs.append (u)
			liste_des_probabilites.append (p)
			liste_des_tuples.append(a)
			print ("liste des probabilites : {0} ".format(liste_des_probabilites))
			#recupere l'utilisateur avec lequel il y a la plus grande affinité.
			
		profile = Profile.objects.get(utilisateur = utilisateur)
		i=1

		#ecriture des proximites de l'utilisateur
		for u, p in liste_des_tuples:
			if Autre_utilisateur.objects.filter(user = u):
				autre_utilisateur = Autre_utilisateur.objects.get(user = u)
				print ("enregistrement numéro {0}".format(i))
				ancienne_proximite=Proximite.objects.filter (profile = profile, Autre_utilisateur =autre_utilisateur)
				if ancienne_proximite:
					ancienne_proximite = Proximite.objects.get (profile = profile, Autre_utilisateur =autre_utilisateur)
					print ("cette proximite existait deja et va etre remplacee par une nouvelle")
					ancienne_proximite.delete()
					proximite = Proximite.objects.create (profile = profile, Autre_utilisateur = autre_utilisateur, proba = p) 
					i = i+1
		

#classer_les_proximites (utilisateur):
	profile = Profile.objects.get(utilisateur =utilisateur)
	print ("profile concerné :{0}".format (profile))
	proximites = Proximite.objects.filter(profile = profile).exclude(Autre_utilisateur__user = utilisateur)
	ancienne_proba_max = 1
	ancien_utilisateur_prefere = utilisateur
	for proximite in proximites:
		print ("proximite concernée :{0}".format (proximite))
		if proximite.proba < ancienne_proba_max:
			ancienne_proba_max = proximite.proba
			ancien_utilisateur_prefere = proximite.Autre_utilisateur.user
			print ("ancien_utilisateur_prefere :{0}".format (ancien_utilisateur_prefere))
	utilisateur_le_plus_proche = ancien_utilisateur_prefere
	propositions_interessantes = Proposition.objects.filter(soutien__user = utilisateur_le_plus_proche).exclude(soutien__user = utilisateur)
	for proposition in propositions_interessantes:
		print ("proposition interessante: {0}".format(proposition.ennonce))



def effacer_proximites():
	proximites =Proximite.objects.all()
	for proximite in proximites:
		proximite.delete()


def simulation1 ():
	liste_personnalite = ["lepen","sarkozy", "bayrou", "hollande", "melanchon"]
	liste_ennonce = ["s'en foutre de la planete", "faire comme si on s'en préoccupait de la planete", "se préoccuper de la planete", "faire de la planete sa priorité"] 
	"""for personnalite in liste_personnalite:
		utilisateur = User.objects.create (username = personnalite)
		utilisateur.save()
		autre_utilisateur = Autre_utilisateur.objects.create (user = utilisateur)
		autre_utilisateur.save()
		profile = Profile.objects.create (utilisateur = utilisateur)
		profile.save()"""
	for ennonce in liste_ennonce:
		proposition = Proposition.objects.create(ennonce = ennonce)


def simulation2():
	utilisateurs = User.objects.all().exclude(username ="nicolas").exclude(username = "nico")
	for utilisateur in utilisateurs:
		utilisateur.set_password("chienchat")
		utilisateur.password.save()



