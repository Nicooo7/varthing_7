#graphiques_des_propositions

import networkx as nx



def creer_un_dictionnaire_proposition_soutiens (propositions):
	dictionnaire_des_propositions = {}
	for proposition in propositions :
		soutiens = Soutien.objects.filter(propositions__id = proposition.id)
		dictionnaire_des_propositions[proposition.id]=soutiens
	return dictionnaire_des_propositions




def lister_les_couples_de_proposition(propositions):
	liste_des_couples = []
	for proposition1 in propositions:
		for proposition2 in propositions:
			if proposition1 != proposition2:
				couple = (proposition1, proposition2)
					liste_des_couples.append(couple)
	return liste_des_couples




def nb_utilisateur_communs_de_2_propositions(proposition1, proposition2, dictionnaire_des_propositions):
	liste_commune = []
	soutiens1 = dictionnaire_des_propositions[proposition1]
	soutiens2 = dictionnaire_des_propositions[proposition2]
	for soutien_a in soutiens1:
		if soutien_a in soutiens2:
			liste_commune.append(soutien_a)
	return len(liste_commune)




def creer_les_noeuds(G, propositions):
	for proposition in propositions:
		G.add_node(proposition)


def creer_les_liens (G, liste_des_couples):
	for couple in liste_des_couples:
		force = nb_utilisateur_communs_de_2_propositions(*couple)
		G.add_edge(*couple, weight = force)


G = nx.Graph()
propositions = Proposition.objects.all()
dictionnaire_des_propositions = creer_un_dictionnaire_proposition_soutiens(propositions)
liste_des_couples = lister_les_couples_de_proposition(propositions)

creer_les_noeuds(G, propositions)
creer_les_liens (G, liste_des_couples)

nx.write_gexf(G, "propositions.gexf")








