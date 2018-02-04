from django.contrib import admin

from .models import Proposition
from .models import Theme
from .models import Lieu
from .models import Profile
from .models import Soutien
from .models import Proximite
from .models import Autre_utilisateur
from .models import Organisation
from .models import Evenement
from .models import Proximite
from .models import Petition
from .models import Competence
from .models import Document
from .models import Organisation


class SoutienAdmin(admin.ModelAdmin):
	list_display	= ('user', 'date', 'lien', 'propositions', 'evenement', 'organisation', 'petition', 'competence', 'document')
	list_filter		= ('user', 'date', 'lien', 'propositions', 'evenement', 'organisation', 'petition', 'competence', 'document')
	date_hierarchy	= 'date'
	ordering		= ('user', 'date', 'lien', 'propositions', 'evenement', 'organisation', 'petition', 'competence', 'document')
	search_fields	= ('user', 'date', 'lien', 'propositions', 'evenement', 'organisation', 'petition', 'competence', 'document')

class PetitionAdmin(admin.ModelAdmin):
	list_display	= ('titre', 'date_creation', 'date_echeance', 'objectif_de_signataires')

class CompetenceAdmin(admin.ModelAdmin):
	list_display	= ('titre', 'date_creation', 'date_echeance')

class EvenementAdmin(admin.ModelAdmin):
	list_display	= ('titre', 'lieu', 'date', 'description', 'proposition', 'participants')

class DocumentAdmin(admin.ModelAdmin):
	list_display	= ('nom', 'date_creation', 'fichier', 'proposition')

class OrganisationAdmin(admin.ModelAdmin):
	list_display	= ('description', 'date_creation', 'nom', 'mail_contact', 'url_du_site')


admin.site.register(Proposition)
admin.site.register(Theme)
admin.site.register(Lieu)
admin.site.register(Profile)
admin.site.register(Soutien, SoutienAdmin)
admin.site.register(Autre_utilisateur)
admin.site.register(Proximite)
admin.site.register(Evenement)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(Organisation, OrganisationAdmin)


