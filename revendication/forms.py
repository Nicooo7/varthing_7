from django import forms
from django.forms import ModelForm, Textarea
from .models import *
from .views import *


liste_des_themes = Theme.objects.all()
liste_des_intitules = [("aucun","aucun")]
for theme in liste_des_themes:
	intitule = theme.intitule 
	couple = (intitule,intitule)
	liste_des_intitules.append(couple)


class RevendicationForm(forms.Form):	

	liste_des_themes = Theme.objects.all()
	liste_des_intitules = [("aucun","aucun")]
	for theme in liste_des_themes:
		intitule = theme.intitule 
		couple = (intitule,intitule)
		liste_des_intitules.append(couple)


	intitule = forms.CharField(max_length=100)
	theme_existant = forms.ChoiceField(choices = liste_des_intitules)
	nouveau_theme = forms.CharField (max_length=100)
	print (liste_des_intitules)


class ProfilForm(forms.Form):

	homme_femme = [("homme","homme"), ("femme","femme")]

	mail = forms.EmailField(max_length = 254)
	age = forms.IntegerField()
	sexe = forms.MultipleChoiceField(choices = homme_femme)
	profession = forms.CharField(max_length = 10)
	interets = forms.CharField (max_length = 1000)



class UtilisateurForm(forms.Form):
	nom = forms.CharField(max_length=100)
	mot_de_passe = forms.CharField(max_length=100)
	mail = forms.EmailField(max_length=254)


class OrganisationForm(forms.Form):
	nom = forms.CharField(max_length=100)
	mot_de_passe = forms.CharField(max_length=100)
	mail = forms.EmailField(max_length=254)
	description =  forms.CharField(max_length=10000)

class EvenementForm(forms.Form):
	titre = forms.CharField (max_length = 100)
	date = forms.DateField ()
	description = forms.CharField(widget=forms.Textarea, max_length = 10000)

class PetitionForm(forms.Form):
	"""
	"""
	titre = forms.CharField(max_length = 100)
	description = forms.CharField(widget = forms.Textarea)
	#propositions = forms.CharField(widget = )
	date_echeance = forms.DateField(required = False)
	objectif_de_signataires = forms.IntegerField(required = False, min_value = 0)
	"""
	class Meta:
		model = Petition
		#fields = ['titre', 'description', 'propositions', 'date_echeance', 'objectif_de_signataires']
		fields = '__all__'
	"""

class CompetenceForm(forms.Form):
	"""
	"""
	titre = forms.CharField(max_length = 100)
	description = forms.CharField(widget = forms.Textarea)
	#propositions = forms.CharField(widget = )
	date_echeance = forms.DateField(required = False)
	"""
	class Meta:
		model = Petition
		#fields = ['titre', 'description', 'propositions', 'date_echeance', 'objectif_de_signataires']
		fields = '__all__'
	"""
		

class AuthentificationForm(forms.Form):
	nom = forms.CharField(max_length=100)
	mot_de_passe = forms.CharField(max_length=100)

