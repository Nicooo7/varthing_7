# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist


from .forms import *
from .models import *
from django.contrib.auth.models import* 
from django.contrib.auth import *
from bs4 import BeautifulSoup
from django.template.response import *
from datetime import *
import bs4
import re
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup
from random import *
from .creation_graph import *
from unidecode import unidecode
from django.utils.safestring import mark_safe




app_name = 'revendication'






#_____________________vue_______________________#



def page_accueil(request):
	if request.user.is_authenticated:
		pass
	else:
		return render(request, 'revendications/varthing.html')
	from django.contrib.auth.models import User
	utilisateur = request.user


	def creer_les_evenements_du_calendriers ():

		evenements = Evenement.objects.all()
		fichier_evenement = u""
		for evenement in evenements:
			ligne =  evenement.titre + "/" + str(evenement.date) + "/" + str(evenement.id) + "/" + str(evenement.description) +"ggg" 
			fichier_evenement = fichier_evenement + ligne



		fichier_evenement = unidecode(fichier_evenement).encode("utf-8")
		#print ("************************** fichier_evenement", fichier_evenement)
		return fichier_evenement


	def revendications():
		propositions = Proposition.objects.all()
		mes_propositions = Proposition.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
		date_M1 = datetime.now()-timedelta(30)
		liste= []
        #progression?
		for p in propositions:
			soutiens_M1 = Soutien.objects.filter(date__lte = date_M1, propositions = p)
			nb_soutiens = len(soutiens_M1)
			p.progression = nb_soutiens
			liste.append(p)
			if p in mes_propositions:
				p.mienne = "oui"
			else:
				p.mienne = "non"
		#print("liste______", liste)
		return liste 
		
			


	def documents():
		documents = Document.objects.all()
		return documents 		

		

	def evenements():
		liste_de_mes_evenements = Evenement.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		evenements = Evenement.objects.all()
		liste = []
		for ev in evenements:
			if ev in liste_de_mes_evenements:
				ev.mienne = "oui"
			else:
				ev.mienne = "non"
			liste.append(ev)
		return liste


	def competences():
		liste_de_mes_competences = Competence.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		competences = Competence.objects.all()
		liste = []
		for comp in competences:
			if comp in liste_de_mes_competences : 
				comp.mienne = "oui"
			else:
				comp.mienne = "non"
			liste.append(comp)
		return liste

	
	def organisations():
	#creer la liste des organisations dont je soutiens les propositions
		liste_de_mes_organisations = Organisation.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		organisations = Organisation.objects.all()
		liste = []
		for org in organisations:
			if org in liste_de_mes_organisations:
				org.mienne = "oui"
			else:
				org.mienne = "non"
			liste.append(org)
		return liste	


	def petitions():
		liste_de_mes_petitions = Petition.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		petitions = Petition.objects.all()
		liste = []
		for p in petitions:
			if p in liste_de_mes_petitions : 
				p.mienne = "oui"
			else:
				p.mienne = "non"
			liste.append(p)
		return liste	


		
	
	class formulaire:
		def __init__ (self):
			self.revendication = RevendicationForm
			self.petition =PetitionForm
			self.evenement= EvenementForm
		


	def trier_les_elements_par_dates(liste):
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
			


	def creer_les_datas(utilisateur):

		class Datas:
			def __init__ (self):
				self.evenements = evenements()
				self.competences = competences()
				self.documents = documents()
				self.petitions = petitions()
				self.revendications = revendications()
				self.organisations = organisations()
				self.suggestions = self.revendications


				#formulaires:
				class formulaire:
					def __init__ (self):
						self.revendication = RevendicationForm
						self.petition =PetitionForm
						self.evenement= EvenementForm
				self.formulaires = formulaire()
				


		datas = Datas()
		return datas



	datas = creer_les_datas(utilisateur)

	try:
		onglet = request.session["onglet"]
	except:
		onglet = "vide"

	
	graph_a =  graph_accueil()
	
	
	request.session['message']="vide"
	request.session["proposition_id"]="toutes"

	message = request.session['message']
	return render(request, 'revendications/page_accueil.html', {"datas":datas, "graph_accueil":mark_safe(graph_a),"onglet": onglet, "message":mark_safe(message)})





	
	


	





