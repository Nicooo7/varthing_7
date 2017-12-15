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
		proposition_id = request.GET["proposition_id"]
		proposition = Proposition.objects.get(id = proposition_id)	
		return proposition
	else:
		return "vide"

def retourner_la_petition(request):
	app_name = 'revendication'
	if request.GET:
		petition_id = request.GET["petition.id"]
		petition = Petition.objects.get(id = petition_id)	
		return petition
	else:
		return "vide"

def retourner_evenement(request):
	app_name = 'revendication'
	if request.GET:
		evenement_id = request.GET["evenement_id"]
		evenement = Evenement.objects.get(id = evenement_id)	
		return evenement
	else:
		return "vide"



def supprimer_soutien_revendication(request):
	proposition_id = request.GET["proposition_id"]
	proposition =retourner_la_proposition(request)
	utilisateur= request.user
	liste = []
	soutien = Soutien.objects.get(propositions = proposition, user=utilisateur, lien="SO")
	soutien.delete()
	request.session["onglet"]="revendication"
	proposition = request.GET["proposition_id"]

	if request.GET ['page'] == "revendication":
		return redirect ('page_revendication.html?proposition_id='+ proposition_id)
	else:	
		return redirect ('page_tableau_de_bord.html')


def supprimer_soutien_petition(request):
	proposition_id = request.GET["proposition_id"]
	petition =retourner_la_petition(request)
	utilisateur= request.user
	liste = []
	soutien = Soutien.objects.get(petition = petition, user=utilisateur, lien="SO")
	soutien.delete()
	request.session["onglet"]="petition"
	proposition = request.GET["proposition_id"]
	if request.GET ['page'] == "revendication":
		return redirect ('page_revendication.html?proposition_id='+ proposition_id)
	else:	
		return redirect ('page_tableau_de_bord.html')
	

def supprimer_soutien_evenement(request):
	proposition_id = request.GET["proposition_id"]
	evenement =retourner_evenement(request)
	utilisateur= request.user
	liste = []
	soutien = Soutien.objects.get(evenement= evenement, user=utilisateur, lien="SO")
	soutien.delete()
	request.session["onglet"]="evenement"
	proposition = request.GET["proposition_id"]
	try:
		if request.GET ['page'] == "revendication":
			return redirect ('page_revendication.html?proposition_id='+ proposition_id)
		else:	
			return redirect ('page_tableau_de_bord.html')
	except:
		return redirect ('page_tableau_de_bord.html')		

