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

		evenements = Evenement.objects.filter(soutien__user = utilisateur, soutien__lien = 'SO')
		fichier_evenement = u""
		for evenement in evenements:
			ligne =  evenement.titre + "/" + str(evenement.date) + "/" + str(evenement.id) + "/" + str(evenement.description) +"ggg" 
			fichier_evenement = fichier_evenement + ligne



		fichier_evenement = unidecode(fichier_evenement).encode("utf-8")
		#print ("************************** fichier_evenement", fichier_evenement)
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
		#print ("les revendications les plus populaires",selection)
		return selection



	def les_evenements_les_plus_populaires():
		liste_de_mes_evenements = Evenement.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		evenements = Evenement.objects.all()
		l_evenements = []
		for ev in evenements:
			if ev.proposition in liste_de_mes_propositions:
				l_evenements.append(ev)
		#print("la liste d'evenement", l_evenements)
		liste = []
		for e in l_evenements:
			soutiens = Soutien.objects.filter(evenement = e, lien = 'SO')
			i= 0
			for s in soutiens:
				i += 1
			liste.append((e,i))
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
		#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ liste",liste)
		selection = []
		for element in liste:
			if element[0] not in liste_de_mes_evenements:
				selection.append(element[0])
		#print("les evenements les plus populaires:", selection)
		return selection


	def les_petitions_les_plus_populaires():
		liste_de_mes_petitions = Petition.objects.filter(soutien__user = utilisateur)
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		petitions = Petition.objects.all()
		l_petitions = []
		for p in petitions:
			if p.propositions in liste_de_mes_propositions:
				l_petitions.append(p)
		print("la liste des pétitions", l_petitions)
		liste = []
		for e in petitions:
			soutiens = Soutien.objects.filter(petition = e, lien = 'SO')
			i= 0
			for s in soutiens:
				i += 1
			liste.append((e,i))
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
		#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ liste",liste)
		selection = []
		for element in liste:
			if element[0] not in liste_de_mes_petitions:
				selection.append(element[0])
		print("les petitions les plus populaires:", selection)
		return selection



	def onglet_populaire(x):
		evenements = les_evenements_les_plus_populaires()[0:x]
		#print("evenements", evenements)	
		propositions = les_revendications_les_plus_populaires()[0:x]
		#print("propositions", propositions)
		petitions = les_petitions_les_plus_populaires()[0:x]
		evenements.extend(propositions)
		evenements.extend(petitions)

		print("liste_onglet populaire :",evenements)
		return(evenements)


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
		

		#print ("______________", selection2)
		return selection2[0:n]	



	def trier_les_elements_par_dates(liste):
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
			




	def creer_les_datas(utilisateur):

		class Datas:
			def __init__ (self):
				self.evenements = Evenement.objects.filter(soutien__user = utilisateur, soutien__lien = 'SO')
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
				self.populaire = onglet_populaire(2)
		
		datas = Datas()
		return datas



	datas = creer_les_datas(utilisateur)
	
	graph_u = graph_utilisateur(utilisateur)
	graph_a =  graph_accueil()
	graph_p = graph_populaire()


	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas, "graph_utilisateur":mark_safe(graph_u),"graph_accueil":mark_safe(graph_a),"graph_populaire":mark_safe(graph_p)})

























