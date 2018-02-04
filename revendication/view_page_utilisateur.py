# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .forms import *

#from django.core.exceptions import ObjectDoesNotExist


from revendication.models import *
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
from datetime import datetime
from datetime import timedelta
from .creation_graph import *
from unidecode import unidecode

page = []
liste_des_elements_de_page = []


app_name = 'revendication'


#__________________vues _______________________



def authentification(request):
	
	if request.method == 'POST':
		form = AuthentificationForm(request.POST)
		if form.is_valid():
			username = request.POST["nom"]
			password = request.POST["mot_de_passe"]
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				print ("authentification réussie")
				return redirect ('page_accueil')
				
			else:
				form = AuthentificationForm()		
				return render(request, 'revendications/page_authentification.html', {'form': form})
		else:
			form = AuthentificationForm()
	else:		
		form = AuthentificationForm()		
		return render(request, 'revendications/page_authentification.html', {'form': form})




def se_connecter_comme_organisation(request):
	organisation_id = request.GET["organisation_id"]
	organisation = Organisation.objects.get(id= organisation_id)
	u = organisation.utilisateur
	username = str(u.username)
	
	if request.method == 'POST':
		form = Authentification_organisationForm(request.POST)
		print("FORM", form)
		if form.is_valid():
			print("FORMULAIRE VALIDE")
			password = request.POST["mot_de_passe"]
			print ("PASSWORD:", password)
			print ("USERNAME:", username)
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				print ("authentification réussie")
				return redirect ('page_accueil')
			else: 
				print("ECHECH D'AUTHENTIICATION")
				
		else:
			print("FORMULAIRE NON VALIDE")
			form = Authentification_organisationForm()		
			return render(request, 'revendications/page_authentification_organisation.html', {'form': form, "id" : organisation_id})
		
	else:		
		form = Authentification_organisationForm()		
		return render(request, 'revendications/page_authentification_organisation.html', {'form': form, "id" : organisation_id})




def deconnexion (request):
	from django.contrib.auth import logout
	from django.shortcuts import render
	from django.core.urlresolvers import reverse
	logout(request)
	return redirect ('page_accueil')







def creer_utilisateur (request):
	if request.method == 'POST':
		form = UtilisateurForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur)

			return render(request, 'revendications/page_accueil.html')
	else:
			form = UtilisateurForm()
	
	titre = "nouvel utilisateur"
	return render(request, 'revendications/page_creer.html', {'form': form, "titre": titre, "url" : "page_creer_utilisateur"})
	





