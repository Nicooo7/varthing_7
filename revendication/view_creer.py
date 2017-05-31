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


app_name = 'revendication'



#___________________fonctions__________________#




#_____________________vue_______________________#



    	

def creer_une_revendication (request):
	


	utilisateur= request.user
	
	if request.method == 'POST':
		form = RevendicationForm(request.POST)

		if form.is_valid() :
			
			#si le theme n'existait pas, on en crée un, on l'enregistre et on le garde en variable	
			if request.POST["theme_existant"] == "aucun":
				intitule_du_theme = request.POST["nouveau_theme"]
				theme = Theme (intitule = intitule_du_theme)
				liste_des_themes_existants = Theme.objects.filter(intitule = intitule_du_theme)
				for element in liste_des_themes_existants:
					element.delete()
				theme.save()
			
			#si le thème existait, on le récupère en variable
			else:
				theme = Theme.objects.get(intitule = request.POST["theme_existant"])
			
			#on crée la proposition avec le thème en variable 
			la_proposition = Proposition.objects.create(ennonce = request.POST["intitule"], categorie=theme) 
			la_proposition.save()
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'CR')
			le_soutien.save()
			print ("soutien ajouté:{0} ".format(la_proposition.supporter))
			request.path = "revendications/mes_revendications.html"

			#on affiche la page "mes revendications"
			utilisateur = request.user
			propositions = Proposition.objects.filter(soutien__user= utilisateur)
			propositions2 = Proposition.objects.filter (soutien__user = utilisateur)
			num = 0
			return render (request, 'revendications/mes_revendications.html', {"propositions" : propositions, "propositions2" : propositions2, 'choix_menu': "militer", 'num':num})		
			
	else:
		liste = ""
		form = RevendicationForm()
		propositions = Proposition.objects.all()
		for proposition in propositions:
			ennonce = proposition.ennonce
			liste = liste + ennonce + "_"


		return render(request, 'revendications/page_creer_une_revendication.html', {'form': form, "liste" : liste})
	

