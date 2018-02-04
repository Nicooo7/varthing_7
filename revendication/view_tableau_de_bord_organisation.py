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



def tableau_de_bord_organisation(request):
	

	utilisateur = request.user
	organisation_id = request.GET["organisation_id"]
	organisation = Organisation.objects.get(id=organisation_id)


	def creer_les_evenements_du_calendriers ():

		evenements = organisation.evenement.all()
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
		mes_propositions = organisation.proposition.all()
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


	def suggestions():
		#les utilisateurs proches de moi
		utilisateurs = User.objects.all()
		mes_propositions = organisation.proposition.all()
		liste_des_propositions_communes = []
		liste_des_proximites =[]
		liste = []
		date_M1 = datetime.now()-timedelta(30)

		for u in utilisateurs:
			propositions_u = Proposition.objects.filter(soutien__user=u, soutien__lien="SO")
			for p in propositions_u:
				if p in mes_propositions:
					if p not in liste_des_propositions_communes:
						liste_des_propositions_communes.append(p)
			nb_propositions_communes = len(liste_des_propositions_communes)
			try:
				proximite = nb_propositions_communes/(len(mes_propositions)+len(propositions_u))
			except:
				proximite = 0
			for p in propositions_u:
				if p not in mes_propositions:
					p.force_suggestion = proximite
					if p not in liste:
						soutiens_M1 = Soutien.objects.filter(date__lte = date_M1, propositions = p)
						nb_soutiens = len(soutiens_M1)
						p.progression = nb_soutiens
						liste.append(p)		

		liste_evenement = evenements()
		liste_petitions = petitions()
		liste_documents= documents()				

		liste.extend(liste_evenement)
		liste.extend(liste_petitions)
		liste.extend(liste_documents)

		#print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°listelisteliste",liste)

		return liste			


	def documents():
		propositions = organisation.proposition.all()
		liste=[]
		documents = Document.objects.all()
		for d in documents:
			if d.proposition in propositions:
				liste.append(d)
			
		return liste 		

	def mes_revendications():
		propositions = organisation.proposition.all()
		date_M1 = datetime.now()-timedelta(30)
		liste= []
        #progression?
		for p in propositions:
			soutiens_M1 = Soutien.objects.filter(date__lte = date_M1, propositions = p)
			nb_soutiens = len(soutiens_M1)
			p.progression = nb_soutiens
			if p not in liste:
				liste.append(p)	
				
		return liste 	



	def evenements():
		
		liste_de_mes_evenements = organisation.evenement.all()
		liste_de_mes_propositions = organisation.proposition.all()
		
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




	def competences():
		liste_de_mes_competences = organisation.competence.all()
		liste_de_mes_propositions = organisation.proposition.all()
		competences = Competence.objects.all()
		liste = []
		for comp in competences:
			#print("la valeur de P est: ", p)
			propositions = comp.propositions.all()
			for prop in propositions:
				#print("******************************proposition", prop)
				if prop in liste_de_mes_propositions:
					if comp in liste_de_mes_competences : 
						comp.mienne = "oui"
					else:
						comp.mienne = "non"
					liste.append(comp)
		return liste

		


	def petitions():
		liste_de_mes_petitions = organisation.petition.all()
		liste_de_mes_propositions = organisation.proposition.all()
		petitions = Petition.objects.all()
		liste = []
		for p in petitions:
			#print("la valeur de P est: ", p)
			propositions = p.propositions.all()
			for prop in propositions:
				#print("******************************proposition", prop)
				if prop in liste_de_mes_propositions:
					if p in liste_de_mes_petitions : 
						p.mienne = "oui"
					else:
						p.mienne = "non"
					liste.append(p)
		return liste

			


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
				#self.documents = Documents.objects.filter(soutien__user = utilisateur)
				self.competences = competences()
				self.documents = documents()
				self.petitions = petitions()
				self.mes_revendications = mes_revendications()
				self.suggestions = suggestions()
				self.autocompletion = liste_autocompletion()
				self.calendrier = creer_les_evenements_du_calendriers()
				
				#revendications
				self.mes_revendications = mes_revendications()
				self.page = "tableau_de_bord"
				self.page_organisation ="oui"
				self.organisation = organisation

				#formulaires:
				class formulaire:
					def __init__ (self):
						self.revendication = RevendicationForm
						self.petition =PetitionForm
						self.evenement= EvenementForm
						self.organisation = OrganisationForm
				self.formulaires = formulaire()
				


		datas = Datas()
		return datas



	datas = creer_les_datas(utilisateur)

	try:
		onglet = request.session["onglet"]
	except:
		onglet = "vide"

	graph_u = graph_utilisateur(utilisateur)
	graph_a =  graph_accueil()
	graph_p = graph_populaire()


	request.session["proposition_id"]="toutes"

	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas, "graph_utilisateur":mark_safe(graph_u),"graph_accueil":mark_safe(graph_a),"graph_populaire":mark_safe(graph_p),"onglet": onglet})


