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

#creation de triplet à utiliser pour affichage graphique de la galaxie des propositions
def creer_les_triplets_selon_la_proximite_des_propositions_selon_les_utilisateurs():

		propositions = Proposition.objects.all()
		liste = []
		#on récupère la liste des soutiens des propositions que l'on veut comparer
		for proposition1 in propositions:
			soutiens1 = Soutien.objects.filter(propositions = proposition1, lien = 'SO')
			liste_soutiens1 = []
			for e in soutiens1:
				liste_soutiens1.append(e.user.username)



				
			for proposition2 in propositions:
				soutiens2 = Soutien.objects.filter(propositions = proposition2, lien = 'SO')
				liste_soutiens2 = []
				for e in soutiens2:
					liste_soutiens2.append(e.user.username)

				if proposition2 != proposition1:

					#on compare ces propositions
					liste_des_soutiens_communs = []
					for soutien in liste_soutiens1:
						"""print ("proposition1:{}".format(proposition1))
						print ("proposition2: {}".format(proposition2))
						print ("soutien1: {}".format(soutien))
						print ("soutiens2: {}".format(liste_soutiens2))"""
						if soutien in liste_soutiens2:
							liste_des_soutiens_communs.append(soutien)
							#print ("liste des soutiens communs : {}".format(liste_des_soutiens_communs))
					proximite = len(liste_des_soutiens_communs)/(len (soutiens1) + len(soutiens2))
					
					triplet = (proposition1, proposition2, proximite)
					liste.append(triplet)
		


		triplets = sorted(liste, key=lambda x: x[2])
		triplets.reverse()
		return triplets




#fonction renvoyant les data en format JSON
def affichage_graphique_de_triplet(triplets, seuil): 

	import networkx as nx
	import matplotlib.pyplot as plt
	
	G = nx.Graph()


	for triplet in triplets:
		try:
			if triplet[2] > seuil: 
				G.add_edge(triplet[0], triplet[1], weight = triplet[2])
				G.add_node(triplet[0])

		except:
			print ("oups, objet vide...")

	pos = nx.spring_layout(G)
	print (pos)

	liste_noeud = []


	#ecriture des noeuds:
	noeuds = "{" + ' "nodes" : ' + "["
	i = "premier"
	for cle, valeur in pos.items():
		
		if i == "premier":
			noeud = "{"  + '"id" : ' + '"' + "{}".format(str(cle)) + '"' + "," + ' "label"  : ' + '"' + "{}".format(cle) + '"' + ","  + '"x" :' + "{}".format(valeur[0]) +  "," + ' "y" : ' + "{}".format (valeur[1]) + ","  + ' "size"  : 3 ' +  "}" 
			noeuds = noeuds + "\n" + noeud
			i = "plus_premier"
		else :
			noeud = "{"  + '"id" : ' + '"' + "{}".format(str(cle)) + '"' + "," + ' "label"  : ' + '"' + "{}".format(cle) + '"' + ","  + '"x" :' + "{}".format(valeur[0]) +  "," + ' "y" : ' + "{}".format (valeur[1]) + ","  + ' "size"  : 3 ' + "}" 
			noeuds = noeuds + "\n" + "," + noeud

	noeuds = noeuds + "],"




	#ecriture des edges:
	edges = '"edges":'  + "["
	i = "premier"
	a = 0
	for triplet in triplets:
		try:
			if triplet[2]>seuil:
				if i == "premier":
					edge = "{"  +  ' "id" : ' + '"' + "{}".format(str(a)) + '"' + ","  + ' "source"  : ' + '"' + "{}".format(triplet[0]) + '"' + ","  + ' "target"  :'  + '"' + "{}".format(triplet[1]) + '"'  + "}" 
					edges = edges + "\n" +  edge
					i= "plus_premier"
					a = a+1

				else:
					print (triplet[2])
					edge = "{"  +  ' "id" : ' + '"' + "{}".format(str(a)) + '"' + ","  + ' "source"  : ' + '"' + "{}".format(triplet[0]) + '"' + ","  + ' "target"  :'  + '"' + "{}".format(triplet[1]) + '"' + "}" 
					print(edge)
					edges = edges + "\n" + "," + edge
					a = a+1
		except:
			print("oups, objet vide pour les edges")

	edges = edges + "] }"

	



	#ecriture des data
	data = noeuds + "\n" + "\n" + edges



	#nx.draw_spring(G, with_labels = True, width = 0.1)
	#path = "/Users/nicolasvinurel/Desktop/graph/graph"
	#plt.savefig(path + ".png")
	#nx.write_gexf(G, path + ".gexf")
	return data
		

def enregistrer_les_datas(data, nom):
	#fichier_data = open("/var/www/revendication/static/{}.json".format(nom), "w")
	#fichier_data.write(data)
	# fichier_data.close()
	fichier_data = open("revendication/static/{}.json".format(nom), "w")
	fichier_data.write(data)
	fichier_data.close()




#_____________________vue_______________________#



    	

def page_revendication(request):

	ennonce = request.GET ['ennonce']
	print (ennonce)
	try:
		proposition = Proposition.objects.get(ennonce = ennonce)
	except Proposition.DoesNotExist:
		raise Http404



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
	


	def data_propositions_proches (proposition):
		liste_proximites = creer_les_triplets_selon_la_proximite_des_propositions_selon_les_utilisateurs()
		#selectionner ce qui concerne cette proposition:
		selection = []
		for triplet in liste_proximites:
			if triplet[0]==proposition:
				if triplet[2] > 0:
					selection.append(triplet)
		print ("selection : " ,selection)
		return selection



	def creer_graph_centre_sur_proposition(proposition):
		triplets = data_propositions_proches(proposition)
		data = affichage_graphique_de_triplet(triplets= triplets, seuil=0)
		enregistrer_les_datas(data = data, nom = "graph_proposition")


	creer_graph_centre_sur_proposition(proposition)	
	data_p= []
	for triplet in data_propositions_proches(proposition):
		data_p.append (triplet[1].ennonce)
	data_proposition = data_proposition (proposition)

	return render (request, 'revendications/page_revendication.html', {"propositions_proches": data_p, "data_proposition":data_proposition})







