# coding: utf-8
from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import *

from . import view_page_revendication
from . import view_accueil
from . import view_tableau_de_bord
from . import view_page_organisation
from . import view_creer
from . import view_page_utilisateur
from . import view_page_action

page =[]
liste_des_elements_de_page = []



urlpatterns = [
	
    
    #nouvelles_vues:
    url(r'^varthing', view_accueil.varthing, name = 'varthing'),
    url(r'^page_revendication', view_page_revendication.page_revendication, name = 'page_revendication'),
    url(r'^page_accueil', view_accueil.accueil, name = 'page_accueil'),
    url(r'^page_tableau_de_bord', view_tableau_de_bord.tableau_de_bord, name = 'page_tableau_de_bord'),
    url(r'^page_organisations', view_page_organisation.page_organisation, name = 'page_organisation'),
    url(r'^page_creer_revendication', view_creer.creer_revendication, name = 'page_creer_revendication'),
    url(r'^page_creer_petition', view_creer.creer_petition, name = 'page_creer_petition'),
    url(r'^page_creer_evenement', view_creer.creer_evenement, name = 'page_creer_evenement'),
    url(r'^page_creer_competence', view_creer.creer_competence, name = 'page_creer_competence'),
    url(r'^page_authentification', view_page_utilisateur.authentification, name = 'page_authentification'),
    url(r'^page_creer_utilisateur', view_page_utilisateur.creer_utilisateur, name = 'page_creer_utilisateur'),
    url(r'^page_deconnexion', view_page_utilisateur.deconnexion, name = 'page_deconnexion'),
    url(r'^page_soutenir_revendication', view_page_action.soutenir_une_revendication, name = 'page_soutenir_revendication'),
    ]





