# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import *
from .models import *
from django.contrib.auth.models import* 
from django.contrib.auth import *
from bs4 import BeautifulSoup
from django.template.response import *
import bs4
import re
import urllib.request
import urllib.parse
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup

page = []
liste_des_elements_de_page = []


app_name = 'revendication'


  #..........................PROPOSITIONS.........................#



class Vocabulaire: #motclé et  son champs lexical.
	
	def __init__(self,motcle):
		base = "http://www.rimessolides.com/motscles.aspx?m="
		motcle = urllib.parse.quote(motcle)
		url = """{base}{motcle}""".format(base =base, motcle = motcle)
		with urllib.request.urlopen(url) as f:
		    print (f)
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
	print ("ca demarre")
	with open('vocabulaire', 'ab') as fichier:
		liste_des_vocabulaires = []
		le_mot = Vocabulaire(mot)
		mon_pickler = pickle.Pickler(fichier)
		print ("c'est ok")
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
		for i in range (1, 10):
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
	for element in tokens:
		filtrat.append(element)
	print ("voici le resultat dans le premier programme {0}".format(filtrat))



def champ_lexical_des_propositions():
	#pour chaque proposition
	propositions = Proposition.objects.all()
	for proposition in propositions:
	#récupérer l'ennoncé de la propostion
		ennonce = proposition.ennonce
		filtrat = []
		filtrer_ennonce(ennonce,filtrat)

		initialiser_le_fichier()

		for mot in filtrat:
			print ("*****************")
			print ("on va enregister le mot {0}".format (mot))
			enregistrer_un_nouveau_mot(mot)
			print ("on a enregistre le mot")
		enregistrer_un_nouveau_mot("fin")

		la_liste_des_vocabulaires = []
		implementer_la_liste_des_vocabulaires (la_liste_des_vocabulaires)
		
		liste = ""
		for une_liste in la_liste_des_vocabulaires:
			for un_mot in une_liste:
				liste = liste + ' ,' + un_mot
		print (liste)

		proposition.champ_lexical = liste
		proposition.save()










#..........................AUTRES.........................#





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


















    #..........................REQUESTS.........................#


def consulter (request):
	utilisateur= request.user
	return render (request, 'revendications/consulter.html', {"choix_menu": "consulter"})

def creation_utilisateur (request):
	if request.method == 'POST':
		form = UtilisateurForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur, organisation = False)

			return render(request, 'revendications/merci.html')
	else:
			form = UtilisateurForm()
	
	return render(request, 'revendications/creation_utilisateur.html', {'form': form, "choix_menu":"adhesion"})
	

def militer (request):
	#champ_lexical_des_propositions()

	return render (request, 'revendications/militer.html', {"choix_menu": "militer"})	

def organiser (request):
	return render (request, 'revendications/organiser.html', {"choix_menu": "organiser"})
		


def authentification(request):
	error = False
	
	if request.method == 'POST':
		form = AuthentificationForm(request.POST)
		if form.is_valid():
			username = request.POST["nom"]
			password = request.POST["mot_de_passe"]
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return render (request, 'revendications/merci.html')	
			else:
				error = True
		else:
			form = AuthentificationForm()

	form = AuthentificationForm(request.POST)		
	return render(request, 'revendications/authentification.html', {'form': form, "choix_menu":"authentification"})


def merci (request):
	return render(request, 'revendications/merci.html')


def deconnexion (request):
	from django.contrib.auth import logout
	from django.shortcuts import render
	from django.core.urlresolvers import reverse
	logout(request)
	return render(request, 'revendications/accueil.html', {"utilisateur":"inconnu"})

def accueil(request):
	from django.contrib.auth.models import User
	utilisateur = request.user.username
	print ("voici l'utilisateur" , utilisateur)
	return render(request, 'revendications/accueil.html', {"utilisateur":utilisateur})


def afficher_accueil_revendiquer (request):
	return render (request, 'revendications/accueil_revendiquer.html')



def mes_revendications (request):
	#supprimer_les_propositions_doublons()
	utilisateur = request.user
	propositions = Proposition.objects.filter(soutien__user= utilisateur).filter(soutien__lien = 'CR')
	propositions2 = Proposition.objects.filter (soutien__user= utilisateur)


	
	#classer_les_proximites):
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

	print ("propositions interessantes :{0}".format(propositions_interessantes))
	return render (request, 'revendications/mes_revendications.html', {"propositions" : propositions, "propositions2" : propositions2, 'choix_menu': "militer", "propositions_interessantes": propositions_interessantes , "utilisateur_le_plus_proche": utilisateur_le_plus_proche})
	

def affiche(mot):
	print ("voici l'élément demandé : {0}".format(mot))


def creer_une_revendication (request):


	utilisateur= request.user
	
	if request.method == 'POST':
		form = RevendicationForm(request.POST)

		if form.is_valid() :
			
			#si le theme n'existait pas, on en crée un, on l'enregistre et on le garde en variable	
			if request.POST["theme_existant"] == "aucun":
				intitule_du_theme = request.POST["nouveau_theme"]
				theme = Theme (intitule = intitule_du_theme)
				liste_des_themes_existants = Theme.objects.filter(intitule = intitule_du_theme)
				for element in liste_des_themes_existants:
					element.delete()
				theme.save()
			
			#si le thème existait, on le récupère en variable
			else:
				theme = Theme.objects.get(intitule = request.POST["theme_existant"])
			
			#on crée la proposition avec le thème en variable 
			la_proposition = Proposition.objects.create(ennonce = request.POST["intitule"], categorie=theme) 
			la_proposition.save()
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'CR')
			le_soutien.save()
			print ("soutien ajouté:{0} ".format(la_proposition.supporter))
			request.path = "revendications/mes_revendications.html"

			#on affiche la page "mes revendications"
			utilisateur = request.user
			propositions = Proposition.objects.filter(soutien__user= utilisateur)
			propositions2 = Proposition.objects.filter (soutien__user = utilisateur)
			num = 0
			return render (request, 'revendications/mes_revendications.html', {"propositions" : propositions, "propositions2" : propositions2, 'choix_menu': "militer", 'num':num})		
			
	else:
		form = RevendicationForm()
		return render(request, 'revendications/creer_une_revendication.html', {'form': form})
	


def consult_revendication (request):
	propositions = Proposition.objects.all

	return render (request, 'revendications/consult_revendication.html', {"propositions" :propositions})

def proposition_detail (request):
	id_proposition = request.GET['nom']
	proposition = Proposition.objects.get(id= id_proposition)
	soutien= Soutien.objects.filter(propositions__id = id_proposition).filter(lien ='SO')
	createur= Soutien.objects.filter(propositions__id = id_proposition).filter(lien = 'CR')
	evenement = Evenement.objects.filter (proposition_id = id_proposition)

	print (proposition)
	return render (request, 'revendications/proposition_detail.html', {"createur" :createur, "proposition" :proposition, "soutien" :soutien, "evenement": evenement})	


def soutenir_une_revendication (request):
	utilisateur = request.user
	id_proposition = request.GET['nom']
	proposition = Proposition.objects.get(id= id_proposition)
	Soutien.objects.create(propositions = proposition, user= utilisateur, lien='SO')
	
	request.path ="revendications/mconsult_revendications.html"
	
	propositions = Proposition.objects.all

	return render (request, 'revendications/consult_revendication.html', {"propositions" :propositions})



def afficher_mon_profil (request):
	
	def creer_objet_profil_utilisateur (request):
		utilisateur = request.user
		propositions_soutenues = Proposition.objects.filter (soutien__user= utilisateur)
		militantisme = Militant.objects.filter (utilisateur = utilisateur)
		documents = "vide"
		organisations = "vide"
		actualites = "vide"
		suggestions = "vide"

		class Profil:
			
			def __init__ (self, utilisateur, propositions_soutenues, documents, organisations, actualites, suggestions):
				self.utilisateur = utilisateur
				self.revendications = propositions_soutenues
				self.documents = documents
				self.organisations = militantisme
				self.actualites= actualites
				self.suggestions = suggestions

		profil = Profil(utilisateur, propositions_soutenues, documents, organisations, actualites, suggestions)
		return profil

	profil = creer_objet_profil_utilisateur (request)
	return render (request, 'revendications/afficher_mon_profil.html', {"profil" :profil})


def creer_une_organisation (request):
	if request.method == 'POST':
		form = OrganisationForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			description = request.POST['description']
			organisation = True
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			#autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur)
			organisation = Organisation.objects.create (profile = profile, description= description)
		

			return render(request, 'revendications/merci.html')
	else:
			form = OrganisationForm()
	
	return render(request, 'revendications/creer_une_organisation.html', {'form': form, "choix_menu":"adhesion"})


def afficher_une_organisation (request):

	id_organisation = request.GET['id_organisation']
	utilisateur = User.objects.get (id = id_organisation)
	profil = Profile.objects.get(utilisateur = utilisateur)
	organisation = Organisation.objects.get(profile = profil)


	print ("la description est  : {}".format(organisation.description))
	
	return render(request, 'revendications/afficher_une_organisation.html', {'organisation': organisation, 'profil': profil})



def adherer_a_une_organisation (request):
	id_organisation = request.GET['nom']
	utilisateur = request.user
	organisation = Organisation.objects.get(id = id_organisation)
	soutien = Soutien.objects.create(organisation = organisation, user = utilisateur)
	organisation.soutien = soutien
	organisation.save()

	organisations = Organisation.objects.all

	return render (request, 'revendications/consult_organisations.html', {"organisations" :organisations})
	


def consulter_les_organisations (request):
	organisations = Organisation.objects.all

	return render (request, 'revendications/consult_organisations.html', {"organisations" :organisations})
	


def mes_organisations (request):
	utilisateur = request.user
	organisations = Organisation.objects.filter(soutien__user=utilisateur)
	print ("voici la liste des organisations : {}".format(organisations))
	
	return render(request, 'revendications/mes_organisations.html', {'organisations': organisations})





def creer_un_evenement (request):
	id_proposition = request.GET['id_proposition']

	if request.method == 'POST':
		form = EvenementForm(request.POST)
		if form.is_valid():
			lieu = request.POST['lieu']
			date = request.POST['date']
			description = request.POST['description']

			id_proposition = request.GET['id_proposition']
			proposition = Proposition.objects.get(id = id_proposition)	

			createur = request.user
		
			evenement = Evenement.objects.create (date = date, description = description, proposition =proposition)
			evenement.save()
			soutien = Soutien.objects.create (evenement = evenement, user = createur, lien = 'CR')
			soutien.save()


			return render(request, 'revendications/merci.html')
	else:
		form = EvenementForm()
	
	print ("voici le formulaire = {}".format(form))

	return render(request, 'revendications/creer_un_evenement.html', {'form': form, 'id_proposition':id_proposition})

	
def detail_evenement(request):
	evenement_id = request.GET['id_evenement']
	evenement = Evenement.objects.get(id = evenement_id)
	participants= Soutien.objects.filter (evenement = evenement)

	print ("l'evenement est {}".format(evenement))

	return render(request, 'revendications/detail_evenement.html', {'evenement': evenement, 'participants':participants})



def participer_a_un_evenement (request):
	id_evenement= request.GET['evenement_id']
	utilisateur = request.user
	evenement= Evenement.objects.get(id = id_evenement)
	soutien = Soutien.objects.create(evenement= evenement, user = utilisateur)
	evenement.participant = soutien
	evenement.save()

	organisations = Organisation.objects.all

	return render (request, 'revendications/militer.html', {"choix_menu": "militer"})


def mes_evenements(request):
	utilisateur = request.user
	evenements = Evenement.objects.filter(soutien__user=utilisateur)
	print ("voici la liste des evenements : {}".format(evenements))
	
	return render(request, 'revendications/mes_evenements.html', {'evenements': evenements})


def creer_une_petition():
	print ("en cours.")
















