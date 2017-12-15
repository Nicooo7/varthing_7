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



   	

def page_evenement(request):
	

	evenement_id = request.GET["evenement_id"]
	evenement = Evenement.objects.get(id = evenement_id)
	

	def creer_les_datas(evenement):
		
		utilisateur = request.user

		class Data:
			def __init__ (self):	
				self.evenement = evenement
				try:
					self.createur = str(Soutien.objects.filter(evenement__id = evenement_id).filter(lien = 'CR')[0])
				except:
					self.createur = "inconnu"
				mes_evenements = Evenement.objects.filter(soutien__user = utilisateur, soutien__lien = "SO")
				if evenement in mes_evenements:
					self.soutenue = "oui"
				else:
					self.soutenue = "non"

		data = Data()		
		return (data)


	
	datas = creer_les_datas(evenement)



	return render (request, 'revendications/page_evenement.html', {"datas":datas})