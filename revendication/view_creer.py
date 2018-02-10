# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth.hashers import *
#from django.core.exceptions import ObjectDoesNotExist


from .forms import *
from .models import *
from django.contrib.auth.models import* 
from django.contrib.auth import *
from bs4 import BeautifulSoup
from django.template.response import *
import bs4
import re
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup
from random import *
from unidecode import unidecode



def retourner_la_proposition(request):
	app_name = 'revendication'
	if request.GET:
		ennonce = request.GET["ennonce"]
		proposition = Proposition.objects.get(ennonce)	
		return proposition
	else:
		return "vide"


def creer_document(request):
		#proposition =retourner_la_proposition(request)
	##print ("___________creation evenement_")

	utilisateur= request.user

	proposition_id = request.session["proposition_id"]
	proposition = Proposition.objects.get(id=proposition_id)


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = DocumentForm(request.POST,request.FILES)
		#print("formulaire:", form)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			nom = unidecode(form.cleaned_data['nom']).encode('utf-8')
			format = unidecode(form.cleaned_data['format']).encode('utf-8')
			fichier = request.FILES['fichier']
				
			# Création du document puis association à la proposition source
			document = Document.objects.create(nom=nom, format=format, proposition= proposition, fichier=fichier)

			
			#document.propositions.add(proposition)
			document.save()
			#print("*********************************************************** object enregistré")
			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(document = document, user = utilisateur, lien = 'CR')

			#on retourne à la page accueil
			
			return redirect ('page_revendication.html?proposition_id='+ str(proposition.id))	
		
			
		

			

def creer_revendication(request):

	#proposition =retourner_la_proposition(request)
	utilisateur= request.user

	if request.method == 'POST':
		form = RevendicationForm(request.POST)
		
		if form.is_valid():
			intitule = unidecode(request.POST["intitule"])
			#on crée la proposition 
			la_proposition = Proposition.objects.create(ennonce = intitule, tags=request.POST["tags"]) 
			la_proposition.save()
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'CR')
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'SO')
			le_soutien.save()
			#print ("soutien ajouté:{0} ".format(la_proposition.supporter))

			#on retourne à la page accueil
			return redirect ('page_tableau_de_bord.html')	
			


def creer_petition(request):

	utilisateur= request.user

	if request.user.is_authenticated:
		user = request.user
	else:
		render(request, 'authentification_necessaire.html')


	# Récups des infos GET si transmises
	id_proposition = request.session["proposition_id"]
	proposition = Proposition.objects.get(id=id_proposition)
	


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = PetitionForm(request.POST)
		if form.is_valid():			#
			# Traitement du formulaire valide
			#
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')

			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date_echeance = form.cleaned_data['date_echeance']
			objectif_de_signataires = form.cleaned_data['objectif_de_signataires']

			#propositions = form.cleaned_data['propositions']	

			# Récupération des propositions cochées
			# erreur si liste vide
			"""try:
				propositions = request.POST.getlist('propositions')
			except:
				raise Http404"""

			
			# Création de la pétition puis association à la proposition source
			petition = Petition.objects.create(titre=titre, description=description, date_echeance=date_echeance, objectif_de_signataires=objectif_de_signataires)

	
			
			#petition.propositions.add(proposition)
			petition.save()

			petition.propositions.add(proposition)

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(petition = petition, user = user, lien = 'CR')

			#on retourne à la page accueil
			
			
			return redirect ('page_revendication.html?proposition_id='+ str(proposition.id))



def creer_competence(request):

	utilisateur= request.user

	# Récups des infos GET si transmises
	id_proposition = request.session["proposition_id"]
	proposition = Proposition.objects.get(id=id_proposition)
	
	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = CompetenceForm(request.POST)
		if form.is_valid():
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')
			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date_echeance = form.cleaned_data['date_echeance']
			lieu = unidecode(form.cleaned_data['lieu']).encode('utf-8')
			
			# Création de la compétence puis association à la proposition source
			competence = Competence.objects.create(titre=titre, description=description, date_echeance=date_echeance, lieu=lieu)
			competence.save()
			competence.propositions.add(proposition)

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(competence = competence, user = utilisateur, lien = 'CR')
		

			#on retourne à la page accueil
			return redirect ('page_revendication.html?proposition_id='+ str(proposition.id))

		else: 
			#print("form non valide")
			pass



def creer_evenement(request):

	#proposition =retourner_la_proposition(request)
	##print ("___________creation evenement_")

	utilisateur= request.user

	if request.user.is_authenticated:
		user = request.user
	else:
		#print ('authentification necessaire')
		pass

	proposition_id = request.session["proposition_id"]
	proposition = Proposition.objects.get(id=proposition_id)


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = EvenementForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')
			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date = form.cleaned_data['date']
				

			# Création de l'evenement'puis association à la proposition source
			evenement = Evenement.objects.create(titre=titre, description=description, date=date, proposition = proposition)

			
			#petition.propositions.add(proposition)
			evenement.save()

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(evenement = evenement, user = user, lien = 'CR')

			#on retourne à la page 
			
			return redirect ('page_revendication.html?proposition_id='+ str(proposition.id))	
		



def creer_organisation(request):

	#proposition =retourner_la_proposition(request)
	#print ("___________creation organisation_")

	utilisateur= request.user

	if request.user.is_authenticated:
		user = request.user
	else:
		#print ('authentification necessaire')
		pass

	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = OrganisationForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			nom = unidecode(form.cleaned_data['nom']).encode('utf-8')
			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			url_du_site = unidecode(form.cleaned_data['url_du_site']).encode('utf-8')
			mail_contact = 	unidecode(form.cleaned_data['mail_contact']).encode('utf-8')
			lieu_action = form.cleaned_data['lieu_action']
			mot_de_passe = unidecode(form.cleaned_data['mot_de_passe']).encode('utf-8')
			
			
   
			# Création de l'organisation et des soutiens...

			o = Organisation(nom=nom, description=description, url_du_site=url_du_site, mail_contact = mail_contact)
			utilisateur= User.objects.create_user("organisation_"+str(o.nom), "o.nom@varthing.org", mot_de_passe)
			utilisateur.save()
			o.utilisateur = utilisateur
			o.save()
			
			soutien = Soutien.objects.create(organisation = o, user = user, lien = 'CR')
			soutien.save()

			
			
			
			

			
			#on retourne à la page 
			
		return redirect ('page_tableau_de_bord.html')

