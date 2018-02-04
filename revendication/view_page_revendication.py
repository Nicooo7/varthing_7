# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist

from django.utils.safestring import mark_safe
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
from .creation_graph import *

app_name = 'revendication'


#_____________________vue_______________________#



   	

def page_revendication(request):
	
	try: 
		proposition = Proposition.objects.get(ennonce = str(request.GET["proposition_id"]))
	except:
		proposition = Proposition.objects.get(id= request.GET["proposition_id"])

	def revendications(proposition):
		triplets = data_propositions_proches(proposition)
		liste = []
		for triplet in triplets:
			proposition = Proposition.objects.get(ennonce = triplet[1])
			proposition.score = triplet[2]
			liste.append(proposition)
		return liste

	

	def competence(proposition):
		liste= []
		competences = Competence.objects.all()
		for competence in competences:
			if proposition in competence.propositions.all():
				liste.append(competence)
		return liste

	def petition(proposition):
		liste= []
		petitions = Petition.objects.all()
		for petition in petitions:
			if proposition in petition.propositions.all():
				liste.append(petition)
		return liste	

			


	def creer_les_datas(proposition):
		# Vérification identifiant valide ? si non, 404
		id_proposition = proposition.id
		utilisateur = request.user

		class Data:
			def __init__ (self):	
				self.proposition = proposition
				self.suggestions = revendications(proposition)
				self.soutiens= Soutien.objects.filter(propositions__id = id_proposition).filter(lien ='SO')
				try:
					self.createur= str(Soutien.objects.filter(propositions__id = id_proposition).filter(lien = 'CR')[0])
				#print("jjjqsdfqmsldkfjqmslkdfjqmlskdjfqsjdfmlqskdjflqskjdflqskjdflqksjdflqkjdf createur", self.createur)
				except:
					self.createur = "inconnu"

				self.evenements = Evenement.objects.filter(proposition = proposition)
				self.petitions = petition(proposition)
				self.competences = competence(proposition)
				#self.organisations = organisation(proposition)
				self.documents = Document.objects.filter(proposition = proposition)
				mes_propositions = Proposition.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
				if proposition in mes_propositions:
					self.soutenue = "oui"
				else:
					self.soutenue = "non"

				#formulaires:
				class formulaire:
					def __init__ (self):
						self.revendication = RevendicationForm
						self.petition =PetitionForm
						self.evenement= EvenementForm
						self.competence =CompetenceForm
						self.document = DocumentForm
				self.formulaires = formulaire()
				self.page = "revendication"


		data = Data()		
		return (data)


	
	
	#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", proposition)
	graph = graph_revendication(proposition)
		
	graph = mark_safe(graph)
	datas = creer_les_datas(proposition)
	request.session["proposition_id"]= request.GET["proposition_id"]

	return render (request, 'revendications/page_revendication.html', {"datas":datas, "graph":graph})	






