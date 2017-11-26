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



def tableau_de_bord(request):
	

	utilisateur = request.user


	def creer_les_evenements_du_calendriers ():

		evenements = Evenement.objects.filter(soutien__user = utilisateur, soutien__lien = 'SO')
		fichier_evenement = u""
		for evenement in evenements:
			ligne =  evenement.titre + "/" + str(evenement.date) + "/" + str(evenement.id) + "/" + str(evenement.description) +"ggg" 
			fichier_evenement = fichier_evenement + ligne



		fichier_evenement = unidecode(fichier_evenement).encode("utf-8")
		#print ("************************** fichier_evenement", fichier_evenement)
		return fichier_evenement

#REVENDICATIONS____________________


	def revendications():
		propositions = Proposition.objects.all()
		mes_propositions = Proposition.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
		date_M1 = datetime.now()-timedelta(30)
		liste= []
		#est ce que je soutiens?
		for p in propositions:
			if p in mes_propositions:
				p.mienne = "oui"
			else:
				p.mienne = "non"
        #progression?
			soutiens_M1 = Soutien.objects.filter(date__lte = date_M1, propositions = p)
			nb_soutiens = len(soutiens_M1)
			p.progression = nb_soutiens
			liste.append(p)
		return liste 		


	def revendications_suggestion(n):
		selection = data_propositions_proches_des_miennes(utilisateur)
		selection = sorted(selection, key=lambda x: x[2])
		selection.reverse()
		selection2= []
		liste_p = []
		#print ("******************************************selection:",selection)

		#eliminer les propositions dont je suis déjà supporter
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		for p in liste_de_mes_propositions:
			liste_p.append(p.ennonce)

		#print ("selection:", selection)
		for triplet in selection:
			if triplet[1] in liste_p:
				#print ("le triplet contenant", triplet[1] , "va être enlevé.")
				selection.remove(triplet)
			else:
				if triplet[2] > 0:
					selection2.append(triplet[1])
		

		print ("______________", selection2)
		return selection2[0:n]	



	def revendications_mes_revendications():
		mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		return mes_propositions


	def evenements():
		liste_de_mes_evenements = Evenement.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		evenements = Evenement.objects.all()
		liste = []
		for ev in evenements:
			if ev.proposition in liste_de_mes_propositions:
				if ev in liste_de_mes_evenements:
					ev.mienne = "oui"
				else:
					ev.mienne = "non"
				liste.append(ev)
		return liste


	def petitions():
		liste_de_mes_petitions = Petition.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		petitions = Petition.objects.all()
		liste = []
		for p in petitions:
			print("la valeur de P est: ", p)
			propositions = p.propositions.all()
			for prop in propositions:
				print("******************************proposition", prop)
				if prop in liste_de_mes_propositions:
					if p in liste_de_mes_petitions : 
						p.mienne = "oui"
					else:
						p.mienne = "non"
					liste.append(p)
		return liste



	def retirer_soutien(x):
		soutien = Soutien.objects.get(proposition__id=x, utilisateur = request.user)
		soutien.delete()
			


	def liste_autocompletion():
		liste = u""
		propositions = Proposition.objects.all()
		for proposition in propositions:
			ennonce = proposition.ennonce
			liste = liste + ennonce + u"_"
		liste = unidecode(liste)
		liste = liste.encode("utf-8")
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
				self.mes_evenements = Evenement.objects.filter(soutien__user = utilisateur, soutien__lien = 'SO')
				self.evenements = evenements()
				self.organisations = Organisation.objects.filter(soutien__user = utilisateur)
				#self.documents = Documents.objects.filter(soutien__user = utilisateur)
				self.competences = Competence.objects.filter(soutien__user = utilisateur)
				self.petitions = petitions()
				self.revendications = revendications()
				#self.suggestions = les_x_revendications_les_plus_proches_des_miennes(4)
				#if self.suggestions == []:
				#	self.suggestions = les_revendications_les_plus_populaires()
				self.autocompletion = liste_autocompletion()
				self.calendrier = creer_les_evenements_du_calendriers()
				#revendications
				self.revendications_mes_revendications = revendications_mes_revendications()
				#evenements
			
				#petitions

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

	
	
	graph_u = graph_utilisateur(utilisateur)
	graph_a =  graph_accueil()
	graph_p = graph_populaire()


	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas, "graph_utilisateur":mark_safe(graph_u),"graph_accueil":mark_safe(graph_a),"graph_populaire":mark_safe(graph_p)})

























