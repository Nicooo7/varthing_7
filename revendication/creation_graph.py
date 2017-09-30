# coding: utf-8
from __future__ import division

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist


from revendication.models import *
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
from datetime import datetime
from datetime import timedelta


#print ("DEMARRAGE DE LA CREATION D'UN NOUVEAU GRAPH")

#creation de triplet à utiliser pour affichage graphique de la galaxie des propositions
def creer_les_triplets(): #(selon_mes_propositions_selon_les_utilisateurs)

		propositions = Proposition.objects.all()
		liste = []
		#on récupère la liste des soutiens des propositions que l'on veut comparer
		for proposition1 in propositions:
			soutiens1 = Soutien.objects.filter(propositions = proposition1, lien = 'SO')
			liste_soutiens1 = []
			for e in soutiens1:
				liste_soutiens1.append(e.user.username)
			#print ("soutiens 1", liste_soutiens1, "proposition :" , proposition1 )



				
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
							print ("liste des soutiens communs : {}".format(liste_des_soutiens_communs))
					proximite = len(liste_des_soutiens_communs)/(len (liste_soutiens1) + len(liste_soutiens2))
					#print ("calcul:", len(liste_des_soutiens_communs),len(liste_soutiens1), len(liste_soutiens2), proximite)	
					triplet = (proposition1.ennonce, proposition2.ennonce, proximite)
					#print (triplet)
					if triplet not in liste:
						liste.append(triplet)
		


		triplets = sorted(liste, key=lambda x: x[2])
		triplets.reverse()
		for triplet1 in triplets:
			for triplet2 in triplets:
				if triplet1[0] == triplet2[1]:
					if triplet1[1] == triplet2[0]:
						triplets.remove(triplet1)

		#print ("triplets^^^^^^^^^^^^^^^^^^^^^^^^^",triplets)
		return triplets	


#fonction renvoyant les data en format JSON
def affichage_graphique_de_triplet(triplets, seuil): 

	import networkx as nx
	import matplotlib.pyplot as plt
	
	G = nx.Graph()


	for triplet in triplets:
		G.add_node(triplet[0])
		try:
			if triplet[2] >= seuil: 
				G.add_edge(triplet[0], triplet[1], weight = triplet[2])
		except:
			print ("objet vide")

	pos = nx.spring_layout(G)
	#print (pos)

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
					#print (triplet[2])
					edge = "{"  +  ' "id" : ' + '"' + "{}".format(str(a)) + '"' + ","  + ' "source"  : ' + '"' + "{}".format(triplet[0]) + '"' + ","  + ' "target"  :'  + '"' + "{}".format(triplet[1]) + '"' + "}" 
					#print(edge)
					edges = edges + "\n" + "," + edge
					a = a+1
		except:
			print("objet vide pour les edges")

	edges = edges + "] }"

	



	#ecriture des data
	graph= noeuds + "\n" + "\n" + edges



	#nx.draw_spring(G, with_labels = True, width = 0.1)
	#path = "/Users/nicolasvinurel/Desktop/graph/graph"
	#plt.savefig(path + ".png")
	#nx.write_gexf(G, path + ".gexf")
	return graph
		

def enregistrer_les_datas(data, nom):
	#fichier_data = open("/var/www/revendication/static/revendication/{}.json".format(nom), "w")
	fichier_data = open("revendication/static/revendication/{}.json".format(nom), "w")
	fichier_data.write(data)
	fichier_data.close()



#selectionner parmis les triplets (proposition1,2,lien) ceux concernant mes propositions
def data_propositions_proches_des_miennes (utilisateur):
	liste_proximites = creer_les_triplets()	
	
	

	#recuperer les ennonces de mes propositions
	liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
	liste_ennonces= []
	for proposition in liste_de_mes_propositions:
		p=proposition.ennonce
		liste_ennonces.append(p)

	#selectionner les triplets qui commencent par les ennonces de mes propositions	
	selection = []
	for triplet in liste_proximites:
		proposition1 = triplet[0]
		if proposition1 in liste_ennonces:
			selection.append(triplet)

	#print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$selection" , selection)
	return selection	




def data_propositions_proches (proposition):
	liste_proximites = creer_les_triplets()
	#selectionner ce qui concerne cette proposition:
	selection = []
	for triplet in liste_proximites:
		print (triplet)
		if triplet[0]== proposition.ennonce:
			if triplet[2] > 0:
				selection.append(triplet)
	#print ("selection : " ,selection)
	return selection


#_______________________________________________________________



def graph_accueil():
	triplets = creer_les_triplets()
	data = affichage_graphique_de_triplet(triplets, 0)
	enregistrer_les_datas(data, "graph")


def graph_utilisateur(utilisateur):
	data_propositions_proches = data_propositions_proches_des_miennes(utilisateur)
	graph = affichage_graphique_de_triplet(triplets= data_propositions_proches, seuil=0)
	enregistrer_les_datas(data = graph, nom = "graph")


def graph_revendication(proposition):
	data = affichage_graphique_de_triplet(triplets= data_propositions_proches(proposition), seuil=0)
	enregistrer_les_datas(data = data, nom = "graph")







