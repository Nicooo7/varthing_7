from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import *
from . import views
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
    # Revendications
    url(r'^creer_une_revendication', views.creer_une_revendication, name = 'creer_une_revendication'),
    url(r'^proposition_detail', views.proposition_detail, name = 'proposition_detail'),
    url(r'^consult_revendication', views.consult_revendication, name = 'consult_revendication'),
    url(r'^soutenir_une_revendication', views.soutenir_une_revendication, name = 'soutenir_une_revendication'),
    url(r'^mes_revendications', views.mes_revendications, name = 'mes_revendications'),
    url(r'^voir_revendication', ListView.as_view(model = Proposition), name ='voir_revendication'),
    # Organisations
    url(r'^creer_une_organisation', views.creer_une_organisation, name = 'creer_une_organisation'),
    url(r'^afficher_une_organisation', views.afficher_une_organisation, name = 'afficher_une_organisation'),
    url(r'^consult_organisations', views.consulter_les_organisations, name = 'consult_organisations'),
    url(r'^adherer_a_une_organisation', views.adherer_a_une_organisation, name = 'adherer_a_une_organisation'),
    url(r'^mes_organisations', views.mes_organisations, name = 'mes_organisations'),
    # Evénements
    url(r'^creer_un_evenement', views.creer_un_evenement, name = 'creer_un_evenement'),
    url(r'^detail_evenement', views.detail_evenement, name = 'detail_evenement'),
    url(r'^participer_a_un_evenement', views.participer_a_un_evenement, name = 'participer_a_un_evenement'),
    url(r'^mes_evenements', views.mes_evenements, name = 'mes_evenements'),
    # Pétitions
    url(r'^creer_une_petition', views.creer_une_petition, name = 'creer_une_petition'),
    url(r'^supprimer_une_petition/(\d+)$', views.supprimer_une_petition, name = 'supprimer_une_petition'),
    url(r'^detail_petition/(\d+)$', views.detail_petition, name = 'detail_petition'),
    url(r'^signer_une_petition', views.signer_une_petition, name = 'signer_une_petition'),
    url(r'^mes_petitions', views.mes_petitions, name = 'mes_petitions'),
    # ~ Divers ~
    url(r'^merci', views.merci, name = 'merci'),
    url(r'^message', views.message, name = 'message'),
    ]