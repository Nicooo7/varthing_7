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



   	

def page_organisation(request):
	

	organisation_id = request.GET["organisation_id"]
	organisation = Organisation.objects.get(id = organisation_id)
	

	def creer_les_datas(organisation):
		
		utilisateur = request.user

		class Data:
			def __init__ (self):	
				self.organisation = organisation
				self.propositions = organisation.propositions
				try:
					self.createur = str(Soutien.objects.filter(organisation__id = organisation_id).filter(lien = 'CR')[0])
				except:
					self.createur = "inconnu"
				mes_organisations = Organisation.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
				if organisation in mes_organisations:
					self.soutenue = "oui"
				else:
					self.soutenue = "non"

		data = Data()		
		return (data)


	
	datas = creer_les_datas(organisation)
	request.session["onglet"]="organisation"

	return render (request, 'revendications/page_organisation.html', {"datas":datas})