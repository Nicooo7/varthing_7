from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import *
from . import views
page =[]
liste_des_elements_de_page = []



urlpatterns = [
	
	url(r'^voir_revendication', ListView.as_view(model = Proposition), name ='voir_revendication'),
    url(r'^accueil', views.accueil, name='accueil'),
    url(r'^consulter', views.consulter, name = 'consulter'),
    url(r'^militer', views.militer, name = 'militer'),
    url(r'^organiser', views.organiser, name = 'organiser'),
    url(r'^creer_une_revendication', views.creer_une_revendication, name = 'creer_une_revendication'),
    url(r'^merci', views.merci, name = 'merci'),
     url(r'^creation_utilisateur', views.creation_utilisateur, name = 'creation_utilisateur'),
    url(r'^deconnexion', views.deconnexion, name = 'deconnexion'),
    url(r'^mes_revendications', views.mes_revendications, name = 'mes_revendications'),
    url(r'^authentification', views.authentification, name = 'authentification'),
    url(r'^consult_revendication', views.consult_revendication, name = 'consult_revendication'),
    url(r'^soutenir_une_revendication', views.soutenir_une_revendication, name = 'soutenir_une_revendication'),
    url(r'^proposition_detail', views.proposition_detail, name = 'proposition_detail'),
    ]