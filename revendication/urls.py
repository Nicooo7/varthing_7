# coding: utf-8
from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import *
from . import views
from . import view_page_revendication
from . import view_accueil
from . import view_tableau_de_bord
from . import view_page_organisation
from . import view_creer
page =[]
liste_des_elements_de_page = []



urlpatterns = [
	
    url(r'^$', views.accueil, name='accueil'),
    url(r'^accueil', views.accueil, name='accueil'),
    url(r'^consulter', views.consulter, name = 'consulter'),
    url(r'^militer', views.militer, name = 'militer'),
    url(r'^organiser', views.organiser, name = 'organiser'),
    # Gestion utilisateurs
    url(r'^creation_utilisateur', views.creation_utilisateur, name = 'creation_utilisateur'),
    url(r'^deconnexion', views.deconnexion, name = 'deconnexion'),
    url(r'^authentification', views.authentification, name = 'authentification'),
    url(r'^afficher_mon_profil', views.afficher_mon_profil, name = 'afficher_mon_profil'),
    url(r'^modifier_profil', views.modifier_profil, name = 'modifier_profil'),


    # Revendications
    url(r'^creer_une_revendication', views.creer_une_revendication, name = 'creer_une_revendication'),
    url(r'^proposition_detail/(\d+)$', views.proposition_detail, name = 'proposition_detail'),
    url(r'^consult_revendications', views.consult_revendications, name = 'consult_revendications'),
    url(r'^soutenir_une_revendication/(\d+)$', views.soutenir_une_revendication, name = 'soutenir_une_revendication'),
    url(r'^mes_revendications', views.mes_revendications, name = 'mes_revendications'),
    #  -> USELESS ??? url(r'^voir_revendication', ListView.as_view(model = Proposition), name ='voir_revendication'),
    url(r'^afficher_le_graph_des_propositions', views.afficher_le_graph_des_propositions, name = 'afficher_le_graph_des_propositions'),
    # Organisations
    url(r'^creer_une_organisation', views.creer_une_organisation, name = 'creer_une_organisation'),
    url(r'^afficher_une_organisation', views.afficher_une_organisation, name = 'afficher_une_organisation'),
    url(r'^consult_organisations', views.consulter_les_organisations, name = 'consult_organisations'),
    url(r'^adherer_a_une_organisation/(\d+)$', views.adherer_a_une_organisation, name = 'adherer_a_une_organisation'),
    url(r'^mes_organisations', views.mes_organisations, name = 'mes_organisations'),
    # Evénements
    url(r'^creer_un_evenement', views.creer_un_evenement, name = 'creer_un_evenement'),
    url(r'^detail_evenement/(\d+)$', views.detail_evenement, name = 'detail_evenement'),
    url(r'^participer_a_un_evenement', views.participer_a_un_evenement, name = 'participer_a_un_evenement'),
    url(r'^mes_evenements', views.mes_evenements, name = 'mes_evenements'),

    # Pétitions
    url(r'^creer_une_petition', views.creer_une_petition, name = 'creer_une_petition'),
    url(r'^supprimer_une_petition/(\d+)$', views.supprimer_une_petition, name = 'supprimer_une_petition'),
    url(r'^detail_petition/(\d+)$', views.detail_petition, name = 'detail_petition'),
    url(r'^signer_une_petition', views.signer_une_petition, name = 'signer_une_petition'),
    url(r'^mes_petitions', views.mes_petitions, name = 'mes_petitions'),
    # competence
    url(r'^creer_une_competence', views.creer_une_competence, name = 'creer_une_competence'),
    url(r'^supprimer_une_competence/(\d+)$', views.supprimer_une_competence, name = 'supprimer_une_competence'),
    url(r'^detail_competence/(\d+)$', views.detail_competence, name = 'detail_competence'),
    url(r'^signer_une_competence', views.signer_une_competence, name = 'signer_une_petition'),
    url(r'^mes_competences', views.mes_competences, name = 'mes_competences'),

    #nouvelles_vues:
    url(r'^page_revendication', view_page_revendication.page_revendication, name = 'page_revendication'),
    url(r'^page_accueil', view_accueil.accueil, name = 'page_accueil'),
    url(r'^page_tableau_de_bord', view_tableau_de_bord.tableau_de_bord, name = 'page_tableau_de_bord'),
    url(r'^page_organisations', view_page_organisation.page_organisation, name = 'page_organisation'),
    url(r'^page_creer_revendication', view_creer.creer_une_revendication, name = 'page_creer_revendication'),


    # ~ Divers ~
    url(r'^merci', views.merci, name = 'merci'),
    url(r'^message', views.message, name = 'message'),
    url(r'^auto_completion', views.auto_completion, name = 'auto_completion'),
    url(r'^index2', views.index2, name='index2'),
     url(r'^i2modif', views.index2modif, name='index2modif'),
    url(r'^base2', views.base2, name='base2'),
    ]





