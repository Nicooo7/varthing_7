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



class Revendication:

	def __init__ (self, ennonce, liste_totale_revendications):

		liste_totale_revendications.append(self)

		
		self.ennonce = ennonce

		

		def filtrer1(ennonce):
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
				filtrat.append(element)
			return (filtrat)
		self.liste_mots_cle = filtrer1(ennonce)


		def filtrer2(element):
			base = "http://www.linternaute.com/dictionnaire/fr/definition/"
			url = """ {base}{motcle}""".format(base =base, motcle = element)
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
					resultat = re.match(r"A-Z", element)
					print (resultat)
					if resultat != None:
						print ("le mot contient une majuscule et il s'agit d'un nom propre qu'on va enregistrer")
						filtrat.append(element)
						print ("filtrat :{}".format(filtrat))
			
		
		filtrat =[]			
		for element in self.liste_mots_cle:
			print (element)				
			try:
				filtrer2(element)	
			except:
				try:
					element = element[:-1]
					filtrer2(element)
				except:
					print ("temps pis")	
		print (filtrat)
		self.liste_mots_cle = filtrat





		liste_mots_cle = self.liste_mots_cle
		def vocabulaire(liste_mots_cle):
			#print ("liste de mot cle: {}".format (liste_mots_cle))
			champ_lexical =[]
			for mot_cle in liste_mots_cle:
				#print ("*****************")
				#print (" on s'interesse au mot {}".format (mot_cle))
				base = "http://www.rimessolides.com/motscles.aspx?m="
				url = """ {base}{mot_cle}""".format(base =base, mot_cle = mot_cle)
				with urllib.request.urlopen(url) as f:
					data = f.read().decode('utf-8')
					soup = bs4.BeautifulSoup(data, 'html.parser')
				for section in soup.find_all(class_="Link-MotCle"):
					mot = section.get_text()
					champ_lexical.append(mot) 
				#print ("voici le champ lexical :{} pour le mot : {}".format(champ_lexical, mot_cle))
			
			return champ_lexical
		self.liste_vocabulaire = vocabulaire(liste_mots_cle)
		
		

		#print ("%%%%%%%%%%%%%%%%%%%%")
		liste_vocabulaire = self.liste_vocabulaire


		def enumeration(liste_vocabulaire):
			liste = ""
			for mot in liste_vocabulaire:
				liste = liste + " " + mot
			return (liste)
		self.enumeration_vocabulaire = enumeration (liste_vocabulaire)



		self.liste_des_doublets = []

	def __repr__ (self):
		return (self.ennonce)	

	def __str__(self):	
		return (self.ennonce)



class Paire:

	def __init__ (self, revendication1, revendication2):
		print ("***************** creation d'une paire **************")
		self.revendication1 = revendication1
		#print ("revendication1: {}".format (self.revendication1))
		self.revendication2 = revendication2

		liste_vocabulaire1 = revendication1.liste_vocabulaire
		liste_vocabulaire2 = revendication2.liste_vocabulaire
		self.relation = Relation (liste_vocabulaire1, liste_vocabulaire2)

	def __repr__ (self):
		return "<revendication1 : {} , revendication2: {}, proximite: {}, vocabulaire_commun :{} >".format(self.revendication1, self.revendication2, self.relation.proximite, self.relation.vocabulaire_commun)




class Relation:
	
	def __init__ (self, liste_vocabulaire1, liste_vocabulaire2):

		liste_finale = []



		def vocabulaire_commun(liste_vocabulaire1, liste_vocabulaire2):
			liste = []
			for element in liste_vocabulaire1:
				if element in liste_vocabulaire2:
					#print (element)
					liste.append(element)
			return liste

		self.vocabulaire_commun = vocabulaire_commun (liste_vocabulaire1, liste_vocabulaire2)


		def proximite (vocabulaire_commun):
			nb_element_retenus = len(self.vocabulaire_commun)
			nb_element_liste1 = len(liste_vocabulaire1)
			nb_element_liste2 = len(liste_vocabulaire2)
			nb_element_total = nb_element_liste1 + nb_element_liste2
			proximite = nb_element_retenus/ nb_element_total
			return proximite

		self.proximite = proximite(vocabulaire_commun)





from tkinter import *

class Interface(Frame):
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""

	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, width=20000, height=20000, **kwargs)
		self.pack(fill=BOTH)
		self.nb_clic = 0

		# Création de nos widgets
		self.message_entrez = Label(self, text="entrez la liste des mots ou expressions")
		self.message_entrez.pack()

		self.message_liste = Label(self, text="vous n'avez encore rien entre")
		self.message_liste.pack()

		self.message_proximite = Label(self, text="entrez la liste des mots ou expressions")
		self.message_proximite.pack()

		self.message_vocabulaire = Label(self, text="entrez la liste des mots ou expressions")
		self.message_vocabulaire.pack()

		self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
		self.bouton_quitter.pack(side="left")

		self.bouton_cliquer = Button(self, text="ok", fg="red",
			command=self.cliquer)
		self.bouton_cliquer.pack(side="right")
		
		var_texte1 = StringVar()
		var_texte2 = StringVar()
		var_texte3 = StringVar()
		var_texte4 = StringVar()
		self.ligne_texte1 = Entry(fenetre, textvariable=var_texte1, width=30)
		self.ligne_texte1.pack()

		self.ligne_texte2 = Entry(fenetre, textvariable=var_texte2, width=30)
		self.ligne_texte2.pack()

		self.ligne_texte3 = Entry(fenetre, textvariable=var_texte3, width=30)
		self.ligne_texte3.pack()

		self.ligne_texte4 = Entry(fenetre, textvariable=var_texte4, width=30)
		self.ligne_texte4.pack()
    
	def cliquer(self):
		
		liste_expression = []
		mot = self.ligne_texte1.get()
		if mot != "":
			liste_expression.append(mot)
		mot = self.ligne_texte2.get()
		if mot != "":
			liste_expression.append(mot)
		mot = self.ligne_texte3.get()
		if mot != "":
			liste_expression.append(mot)
		mot = self.ligne_texte4.get()
		if mot != "":
			liste_expression.append(mot)

		self.message_liste["text"] = "la liste des expression est {} ".format(liste_expression)


		

		#on crée la liste des revendications
	
		#liste_revendication = creer_la_liste_des_revendications(liste_de_proposition)	
		
		#on cherche les mots qui appartiennent à toutes les revendications	
def chercher_les_mots_communs_aux_revendications (liste_revendication):
			liste_vocabulaire1 = liste_revendication[0].liste_vocabulaire
			print (liste_vocabulaire1)
			for revendication in liste_revendication:
				liste_vocabulaire2 = revendication.liste_vocabulaire
				relation= Relation (liste_vocabulaire1, liste_vocabulaire2)
				liste_vocabulaire1 =relation.vocabulaire_commun
				proximite_finale = relation.proximite
				print (liste_vocabulaire1)
				print ("******************")



		#on l'affiche dans la fenetre
		#self.message_vocabulaire["text"] = "le vocabulaire commun est {} ".format(liste_vocabulaire1)
		#self.message_proximite["text"] = "la proximite est {} ".format(proximite_finale)
			

def comparaison():
	fenetre = Tk()
	interface = Interface(fenetre)
	interface.mainloop()





liste_de_proposition =[
		"virer tous les immigres de france",
		"permettre aux plus pauvre l'accès aux études supérieures",
		"limiter le nombre de mandat des députés",
		"obliger les députés à être présents à l'assemblée nationale",
		"interdire la chasse"
		"permettre aux chasseurs de prénétrer dans les propriétés privées",
		"créer un jour de deuil national en mémoire au Bataclan",
		"interdire la voiture qui se conduit toute seule",
		"limiter la durée du temps de travail",
		"restreindre les pouvoirs des syndicats",
		"développer de nouvelles méthodes de concertation des citoyens"]


def grouper_les_propositions(liste_de_proposition, liste_totale_revendications):

	def creer_la_liste_des_revendications(liste_de_proposition):
			liste_revendication = []
			for expression in liste_de_proposition:
				revendication = Revendication(expression, liste_totale_revendications)
				liste_revendication.append (revendication)
			return liste_revendication
	liste_des_revendications = creer_la_liste_des_revendications(liste_de_proposition)
	print ("liste_des_revendications : {}".format (liste_des_revendications))
	
	def lister_les_doublets(liste_des_revendications):
		liste_des_doublets = []
		for revendication1 in liste_des_revendications:
			for revendication2 in liste_des_revendications:
				if revendication1 != revendication2:
					doublet = (revendication1, revendication2)
					revendication1.liste_des_doublets.append (doublet)
					if (revendication2, revendication1) not in liste_des_doublets:
						liste_des_doublets.append(doublet)
		return liste_des_doublets
	liste_des_doublets = lister_les_doublets(liste_des_revendications)
	print ("liste_des_doublets : {}".format (liste_des_doublets))

	def creer_les_paires(liste_des_doublets):
		liste_des_paires = []
		for doublet in liste_des_doublets:
			revendication1 = doublet[0]
			revendication2 = doublet [1]
			paire = Paire (revendication1, revendication2)
			liste_des_paires.append(paire)
		return liste_des_paires
	liste_des_paires = creer_les_paires(liste_des_doublets)
	#print ("liste_des_paires : {}".format (liste_des_paires))

	

	def ordonner_les_resultats(liste_des_paires):
		liste_ordonnee=[]
		liste_ordonnee = sorted (liste_des_paires, key = lambda paire: paire.relation.proximite)
		print ("voici la liste ordonnee: {}".format (liste_ordonnee))
		return liste_ordonnee	

	liste_ordonnee = ordonner_les_resultats(liste_des_paires)	
	print (liste_ordonnee[-1])
	print (liste_ordonnee[-2])
	print (liste_ordonnee[-3])
	
	for paire in liste_ordonnee:
		if paire.renvendication1 == "virer tous les immigres de france":
			proximite1.append (paire)
	for paire in proximite1:
		print (paire)


if __name__=="__main__":
	liste_totale_revendications = []
	grouper_les_propositions(liste_de_proposition, liste_totale_revendications)
	proximite1 = []
	for paire in liste_ordonnee:
		if paire.renvendication1 == "virer tous les immigres de france":
			proximite1.append (paire)
	for paire in proximite1:
		print (paire)
	
















