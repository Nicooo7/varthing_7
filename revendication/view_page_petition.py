# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist

from django.utils.safestring import mark_safe
from .forms import *
from .models import *
from .autre import *
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



   	

def page_petition(request):
	
	for petition in Petition.objects.all():
		petition.objectif_de_signataire = 300
		petition.save()

	petition_id = request.GET["petition_id"]
	petition = Petition.objects.get(id = petition_id)
	

	def creer_les_datas(petition):
		
		utilisateur = request.user

		class Data:
			def __init__ (self):	
				self.petition = petition
				self.propositions = petition.propositions.all()
				try:
					self.createur = str(Soutien.objects.filter(petition__id = petition_id).filter(lien = 'CR')[0])
				except:
					self.createur = "inconnu"
				mes_petitions = Petition.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
				if petition in mes_petitions:
					self.soutenue = "oui"
				else:
					self.soutenue = "non"

		data = Data()		
		return (data)


	
	datas = creer_les_datas(petition)

	request.session["onglet"]="petition"
	return render (request, 'revendications/page_petition.html', {"datas":datas})