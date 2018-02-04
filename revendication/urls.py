# coding: utf-8
from django.conf.urls import url, include
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static



from . import view_page_revendication
from . import view_accueil
from . import view_tableau_de_bord
from . import view_page_organisation
from . import view_creer
from . import view_page_utilisateur
from . import view_page_action
from . import view_supprimer
from . import view_page_evenement
from . import view_page_petition
from . import view_tableau_de_bord_organisation
page =[]
liste_des_elements_de_page = []






urlpatterns = [
	
    
    #nouvelles_vues:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^varthing', view_accueil.page_accueil, name = 'varthing'),
    url(r'^page_revendication', view_page_revendication.page_revendication, name = 'page_revendication'),
    url(r'^page_evenement', view_page_evenement.page_evenement, name = 'page_evenement'),
    url(r'^page_petition', view_page_petition.page_petition, name = 'page_petition'),
    url(r'^page_organisation', view_page_organisation.page_organisation, name = 'page_organisation'),
    url(r'^page_accueil', view_accueil.page_accueil, name = 'page_accueil'),
    url(r'^page_tableau_de_bord', view_tableau_de_bord.tableau_de_bord, name = 'page_tableau_de_bord'),
    url(r'^page_gestion_organisation',view_page_utilisateur.se_connecter_comme_organisation, name = 'page_gestion_organisation'),
    url(r'^page_organisations', view_page_organisation.page_organisation, name = 'page_organisation'),
    url(r'^page_creer_revendication', view_creer.creer_revendication, name = 'page_creer_revendication'),
    url(r'^page_creer_document', view_creer.creer_document, name = 'page_creer_document'),
    url(r'^page_creer_petition', view_creer.creer_petition, name = 'page_creer_petition'),
    url(r'^page_creer_evenement', view_creer.creer_evenement, name = 'page_creer_evenement'),
    url(r'^page_creer_competence', view_creer.creer_competence, name = 'page_creer_competence'),
    url(r'^page_creer_organisation', view_creer.creer_organisation, name = 'page_creer_organisation'),
    url(r'^page_authentification', view_page_utilisateur.authentification, name = 'page_authentification'),
    url(r'^page_creer_utilisateur', view_page_utilisateur.creer_utilisateur, name = 'page_creer_utilisateur'),
    url(r'^page_deconnexion', view_page_utilisateur.deconnexion, name = 'page_deconnexion'),
    url(r'^page_soutenir_revendication', view_page_action.soutenir_une_revendication, name = 'page_soutenir_revendication'),
    url(r'^page_soutenir_organisation', view_page_action.soutenir_une_organisation, name = 'page_soutenir_organisation'),
    url(r'^page_supprimer_soutien_revendication', view_supprimer.supprimer_soutien_revendication, name = 'page_supprime_soutien_revendication'),
    url(r'^page_soutenir_petition', view_page_action.soutenir_une_petition, name = 'page_soutenir_petition'),
    url(r'^page_supprimer_soutien_petition', view_supprimer.supprimer_soutien_petition, name = 'page_supprime_soutien_petition'),
    url(r'^page_soutenir_evenement', view_page_action.soutenir_un_evenement, name = 'page_soutenir_evenement'),
    url(r'^page_supprimer_soutien_evenement', view_supprimer.supprimer_soutien_evenement, name = 'page_supprime_soutien_evenement'),
    #url(r'^page_telecharger', view_page_action.telecharger, name = 'page_telecharger'),
    ]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns"""


