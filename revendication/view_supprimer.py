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
from unidecode import unidecode


def retourner_la_proposition(request):
	app_name = 'revendication'
	if request.GET:
		ennonce = request.GET["ennonce"]
		proposition = Proposition.objects.get(ennonce = ennonce)	
		return proposition
	else:
		return "vide"



def supprimer_soutien_revendication(request):


	proposition =retourner_la_proposition(request)
	utilisateur= request.user
	liste = []
	soutien = Soutien.objects.get(propositions = proposition, user=utilisateur, lien="SO")
	soutien.delete()

	return redirect ('page_tableau_de_bord.html')


