# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist

from . import *
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
#from django.utils.safestring import mark_safe
#from colored import colored
#ifrom colored import fore, back, style


app_name = 'revendication'




#_____________________vue_______________________#
def telecharger(request):
	fichier = request.GET['fichier_url'] 
	return redirect(fichier)

def soutenir_un_element (request, element):
	# Vérification identifiant valide ? si non, 404
	try:
		proposition = Proposition.objects.get(id = request.GET["proposition_id"])
	except Proposition.DoesNotExist:
		raise Http404

	utilisateur = request.user

	soutien = Soutien.objects.get_or_create(element = element, user= utilisateur, lien='SO')
	soutien[0].save()
	
	#request.path ="revendications/consult_revendications.html"
	request.session["onglet"]=str(element)


	#On cree un soutien si la proposition en rapport est soutenue par l'utilisateur
	if element.proposition in Proposition.objects.filter(soutien__user = utilisateur):
		soutien = Soutien.objects.get_or_create(element = element, user= utilisateur, lien='SO')
		#print (fore.LIGHT_BLUE + back.RED + style.BOLD + "soutien" + style.RESET)
		soutien[0].save()
		message ="vide"


	#Sinon on renvoi un message d'erreur en expliquant la raison
	else:
		message =  "vous devez soutenir la proposition " + str(element.proposition.ennonce) + " pour pouvoir participer soutenir cet élément"

	
	request.session['message'] = mark_safe(message)
	return retour_vers_page(request)




def soutenir_une_revendication (request):
	# Vérification identifiant valide ? si non, 404	
	
	proposition_id = request.GET["proposition_id"]
	try:
		proposition = Proposition.objects.get(id = request.GET["proposition_id"])
	except Proposition.DoesNotExist:
		raise Http404	

	utilisateur = request.user

	soutien = Soutien.objects.get_or_create(propositions = proposition, user= utilisateur, lien='SO')
	#print ("soutien", soutien)
	soutien[0].save()
	
	#request.path ="revendications/consult_revendications.html"
	request.session["onglet"]="revendication"
	
	if request.GET ['page'] == "revendication":
		return redirect ('page_revendication.html?proposition_id='+ proposition_id )
	else:	
		return redirect ('page_tableau_de_bord.html')


def soutenir_une_organisation (request):
	# Vérification identifiant valide ? si non, 404
	
	organisation_id = request.GET["organisation_id"]
	organisation = Organisation.objects.get(id=organisation_id)
	utilisateur = request.user

	soutenir_un_element(request, organisation)


	"""soutien = Soutien.objects.get_or_create(organisation = organisation, user= utilisateur, lien='SO')
	soutien[0].save()
	

	#On cree un soutien si la proposition en rapport est soutenue par l'utilisateur
	if organisation.proposition in Proposition.objects.filter(soutien__user = utilisateur):
		soutien = Soutien.objects.get_or_create(organisation = organisation, user= utilisateur, lien='SO')
		#print (fore.LIGHT_BLUE + back.RED + style.BOLD + "soutien" + style.RESET)
		soutien[0].save()
		message ="vide"


	#Sinon on renvoi un message d'erreur en expliquant la raison
	else:
		message =  "vous devez soutenir la proposition " + str(organisation.proposition.ennonce) + " pour pouvoir participer soutenir cet élément"

	
	request.session['message'] = mark_safe(message)
	return retour_vers_page(request)

		
	return redirect ('page_tableau_de_bord.html')"""


def soutenir_une_petition (request):
	# Vérification identifiant valide ? si non, 404

	petition_id = request.GET["petition_id"]
	try:
		petition = Petition.objects.get(id = request.GET["petition_id"])
	except Proposition.DoesNotExist:
		raise Http404

	utilisateur = request.user

	soutien = Soutien.objects.get_or_create(petition = petition, user= utilisateur, lien='SO')
	soutien[0].save()
	
	#request.path ="revendications/consult_revendications.html"
	request.session["onglet"]="petition"


	#On cree un soutien si la proposition en rapport est soutenue par l'utilisateur
	for proposition in petition.propositions.all():
		if proposition in Proposition.objects.filter(soutien__user = utilisateur):
			soutien = Soutien.objects.get_or_create(petition = petition, user= utilisateur, lien='SO')
			#print (fore.LIGHT_BLUE + back.RED + style.BOLD + "soutien" + style.RESET)
			soutien[0].save()
			message ="vide"


	#Sinon on renvoi un message d'erreur en expliquant la raison
		else:
			message =  "vous devez soutenir la proposition " + str(proposition.ennonce) + " pour pouvoir participer soutenir cet élément"

	
	request.session['message'] = mark_safe(message)
	return retour_vers_page(request)


#RETOUR VERS LA PAGE
def retour_vers_page(request):
	request.session["onglet"]="evenement"
	try:
		if request.GET ['page'] == "revendication":
			return redirect ('page_revendication.html?proposition_id='+ request.GET["proposition_id"])
		else:	
			return redirect ('page_tableau_de_bord.html',)
	except:	
		return redirect ('page_tableau_de_bord.html')	


def soutenir_un_evenement (request):
	# Vérification identifiant valide ? si non, 404
	
	evenement_id = request.GET["evenement_id"]
	try:
		evenement = Evenement.objects.get(id = request.GET["evenement_id"])
	except Evenement.DoesNotExist:
		raise Http404

	utilisateur = request.user


	#On cree un soutien si la proposition en rapport est soutenue par l'utilisateur
	if evenement.proposition in Proposition.objects.filter(soutien__user = utilisateur):
		soutien = Soutien.objects.get_or_create(evenement = evenement, user= utilisateur, lien='SO')
		#print (fore.LIGHT_BLUE + back.RED + style.BOLD + "soutien" + style.RESET)
		soutien[0].save()
		message ="vide"


	#Sinon on renvoi un message d'erreur en expliquant la raison
	else:
		message =  "vous devez soutenir la proposition " + str(evenement.proposition.ennonce) + " pour pouvoir participer soutenir cet élément"

	
	request.session['message'] = mark_safe(message)
	return retour_vers_page(request)
		

	



def data_proposition(proposition):
	# Vérification identifiant valide ? si non, 404
	id_proposition = proposition.id

	class Data:
		def __init__ (self):	
			self.proposition = proposition
			self.soutiens= Soutien.objects.filter(propositions__id = id_proposition).filter(lien ='SO')
			self.createur= Soutien.objects.filter(propositions__id = id_proposition).filter(lien = 'CR')
			if len(self.createur)<1:
				self.createur = "inconnu"
			self.evenement = Evenement.objects.filter(proposition_id = id_proposition)
			self.petitions = proposition.petition_set.all()
			self.competences = proposition.competence_set.all()
			self.organisations = Evenement.objects.filter(proposition_id = id_proposition)
			#self.documents = proposition.document_set.all()


	data = Data()		
	return (data)


def est_ce_que_je_soutiens(proposition):
	utilisateur = request.user
	supporters = Soutien.objects.filter(propositions = proposition, lien = 'SO')
	for supporter in supporters:
		#print ("supporter" , supporter)
		if utilisateur == supporter.user:
			return "soutenue"

	s = est_ce_que_je_soutiens(proposition)	
	#print ("s", s)


	graph_revendication(proposition)	
	data_p= []
	for triplet in data_propositions_proches(proposition):
		data_p.append (triplet[1])
	data_proposition = data_proposition (proposition)


	if s == "soutenue" :
		return render (request, 'revendications/page_revendication.html', {"propositions_proches": data_p, "data_proposition":data_proposition, "s":s})
	else:
		return render (request, 'revendications/page_revendication.html', {"propositions_proches": data_p, "data_proposition":data_proposition})	













