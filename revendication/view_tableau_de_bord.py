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
		fichier_evenement = u""
		mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		#print ("mes_propositions", mes_propositions)
		evenements = Evenement.objects.all()
		selection = []
		for evenement in evenements:
			#print ("evenement", evenement, "evenement.proposition", evenement.proposition)
			if evenement.proposition in mes_propositions:
				ligne =   evenement.titre + "/" + str(evenement.date) + "ggg" 
				fichier_evenement = fichier_evenement + ligne

		fichier_evenement = unidecode(fichier_evenement).encode("utf-8")
		print ("************************** fichier_evenement", fichier_evenement)
		return fichier_evenement



	def les_revendications_les_plus_populaires():
		

		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)

		propositions = Proposition.objects.all()
		liste = []
		for p in propositions:
			soutiens = Soutien.objects.filter(propositions = p, lien = 'SO')
			i= 0
			for s in soutiens:
				i += 1
			liste.append((p,i))
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
		#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ liste",liste)
		selection = []
		for element in liste:
			if element[0] not in liste_de_mes_propositions:
				selection.append(element[0])





		#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ selection",selection)
		return selection



	def liste_autocompletion():
		liste = u""
		propositions = Proposition.objects.all()
		for proposition in propositions:
			ennonce = proposition.ennonce
			liste = liste + ennonce + u"_"
		liste = unidecode(liste)
		liste = liste.encode("utf-8")
		return liste



	def les_x_revendications_les_plus_proches_des_miennes(n):

		selection = data_propositions_proches_des_miennes(utilisateur)
		selection = sorted(selection, key=lambda x: x[2])
		selection.reverse()
		selection2= []
		liste_p = []
		print ("******************************************selection:",selection)

		#eliminer les propositions dont je suis déjà supporter
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		for p in liste_de_mes_propositions:
			liste_p.append(p.ennonce)

		#print ("selection:", selection)
		for triplet in selection:
			if triplet[1] in liste_p:
				print ("le triplet contenant", triplet[1] , "va être enlevé.")
				selection.remove(triplet)
			else:
				if triplet[2] > 0:
					selection2.append(triplet[1])
		

		print ("______________", selection2)
		return selection2[0:n]	



	def trier_les_elements_par_dates(liste):
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
			




	def creer_les_datas(utilisateur):

		class Datas:
			def __init__ (self):
				self.evenements = Evenement.objects.filter(soutien__user = utilisateur)
				self.organisations = Organisation.objects.filter(soutien__user = utilisateur)
				#self.documents = Documents.objects.filter(soutien__user = utilisateur)
				self.competence = Competence.objects.filter(soutien__user = utilisateur)
				self.petition = Petition.objects.filter(soutien__user = utilisateur)
				self.revendications = Proposition.objects.filter(soutien__user = utilisateur, soutien__lien = 'SO')
				self.suggestions = les_x_revendications_les_plus_proches_des_miennes(4)
				if self.suggestions == []:
					self.suggestions = les_revendications_les_plus_populaires()[0:5]
				self.autocompletion = liste_autocompletion()
				self.calendrier = creer_les_evenements_du_calendriers()
		
		datas = Datas()
		return datas





 

	def creer_graph():
		if request.GET:
			choix = request.GET['choix']
		else:
			choix = "defaut"

		if choix == "utilisateur":
			graph=graph_utilisateur(utilisateur)
		elif choix == "tout":
			graph=graph_accueil()
		elif choix == "defaut":
			graph=graph_accueil()
		elif choix == "populaire":
			graph =graph_populaire()

		
		print ("_________________graph:", graph)
		return graph

	datas = creer_les_datas(utilisateur)
	graph = creer_graph()

	


	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas, "graph":mark_safe(graph)})

























