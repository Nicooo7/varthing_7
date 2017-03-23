from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

 

class Theme(models.Model):

    intitule = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.intitule


    
class Proposition(models.Model):

    ennonce = models.CharField(max_length=200, null=True)
    date_creation = models.DateField (default= timezone.now, null=True)
    categorie =  models.ForeignKey(Theme, null=True, blank = True)
    supporter = models.ManyToManyField(User, through= "Soutien", null =True)
    champ_lexical = models.CharField (max_length = 100000, default = "vide", null = True)

    def __str__(self):
        return self.ennonce


class Lieu (models.Model):
    pays = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    
    def __str__(self):
        return self.ville

class Autre_utilisateur (models.Model):
    user = models.ForeignKey(User, null =True)

    def __str__(self):
        return "utilisateur {0} ".format (self.user)

class Evenement (models.Model):

    titre = models.CharField(max_length = 10000, null = True)
    lieu = models.ForeignKey (Lieu, null=True)
    date = models.DateField (null=True)
    description = models.CharField(max_length = 10000, null = True)
    proposition = models.ForeignKey (Proposition, null=True)
    participants= models.ManyToManyField(User, through= "Soutien", null =True)

    def __str__(self):
        return self.titre

    # Méthode/Propriété : "createur" : donne le username du créateur de la pétition
    def __createur(self):
        soutien = Soutien.objects.get(evenement=self, lien = 'CR')
        return soutien.user
    createur = property(__createur)

     # Méthode/Propriété : "soutien" : donne le username des soutiens de la pétition
    def __soutiens(self):
        soutiens = Soutien.objects.filter(evenement=self, lien = 'SO')
    soutiens = property(__soutiens)
    
    # Méthode/Propriété : "nb_signataires" : donne le nombre de signataires de la pétition
    def __nb_participant(self):
        return Soutien.objects.filter(evenement=self).count()
    nb_participant = property(__nb_participant)


    def get_absolute_url(self):
        #return reverse('detail_petition', args=[str(self.id)])
        return reverse('detail_evenement')



class Profile (models.Model):
    utilisateur = models.ForeignKey(User, null=True)
    lieu = models.ForeignKey (Lieu, null=True)
    theme_favoris = models.CharField(max_length = 200, null = True)
    utilisateurs_proches = models.ManyToManyField (Autre_utilisateur, through ="Proximite")

    def __str__(self):
        return "profile de {0}".format(self.utilisateur)




        
class Organisation (models.Model):
    description = models.CharField(max_length = 200, null = True)
    profile = models.ForeignKey(Profile, null=True)
    adherent =  models.ManyToManyField(User, through= "Soutien", null =True)

    def __str__(self):
        return "organisation {0}".format(self.profile)


######################################################
#
#    Petition
#
######################################################

class Petition(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField("Descrition de la pétition")
    propositions = models.ManyToManyField(Proposition, null=True)
    date_creation = models.DateField("Date de création", auto_now=True)
    date_echeance = models.DateField("Date d'échéance", null=True, blank=True)
    objectif_de_signataires = models.IntegerField(null=True)
    signataires = models.ManyToManyField(User, through="Soutien", null=True)

    
    # Méthode/Propriété : "createur" : donne le username du créateur de la pétition
    def __createur(self):
        soutien = Soutien.objects.get(petition=self, lien = 'CR')
        return soutien.user
    createur = property(__createur)
    
    # Méthode/Propriété : "nb_signataires" : donne le nombre de signataires de la pétition
    def __nb_signataires(self):
        return Soutien.objects.filter(petition=self).count()
    nb_signataires = property(__nb_signataires)

    # Méthode/Propriété : "taux_objectif" : donne le pourcentage de signature par rapport à l'objectif fixé (renvoi null si pas d'objectif fixé)
    def __taux_objectif(self):
        if self.objectif_de_signataires != 0:
            return Soutien.objects.filter(petition=self).count() / self.objectif_de_signataires * 100
        else:
            return null
    taux_objectif = property(__taux_objectif)

    def get_absolute_url(self):
        #return reverse('detail_petition', args=[str(self.id)])
        return reverse('detail_petition')

    def __str__(self):
        return self.titre


class Competence (models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField("Descrition de la compétence recherchée")
    propositions = models.ManyToManyField(Proposition, null=True)
    date_creation = models.DateField("Date de création", auto_now=True)
    date_echeance = models.DateField("Date d'échéance", null=True, blank=True)
    personnes = models.ManyToManyField(User, through="Soutien", null=True)

    
    # Méthode/Propriété : "createur" : donne le username du créateur de la pétition
    def __createur(self):
        soutien = Soutien.objects.get(competence=self, lien = 'CR')
        return soutien.user
    createur = property(__createur)
    

    def get_absolute_url(self):
        #return reverse('detail_petition', args=[str(self.id)])
        return reverse('detail_petition')

    def __str__(self):
        return self.titre


class Soutien(models.Model):

    CHOIX_LIEN= (
                ('CR' , 'createur'),
                ('SO', 'soutien')
    )
    propositions = models.ForeignKey(Proposition, null =True)
    user = models.ForeignKey(User, null=True)
    lien = models.CharField(max_length =2, choices= CHOIX_LIEN)
    date = models.DateField("Date création soutien", auto_now=True)

    # Elément soutenu
    evenement = models.ForeignKey(Evenement, null = True)
    organisation = models.ForeignKey(Organisation, null = True)
    petition = models.ForeignKey(Petition, null = True)
    competence = models.ForeignKey(Competence, null = True)

    def __str__(self):
        return self.user.username
        #return "lien entre {0} et {1}{2}{3} (type {4})".format(self.user, self.evenement, self.organisation, self.petition, self.lien)



class Proximite(models.Model):
    profile = models.ForeignKey(Profile, null =True)
    Autre_utilisateur = models.ForeignKey (Autre_utilisateur)
    proba = models.DecimalField( max_digits=5, decimal_places=3)

    def __str__(self):
        return "proximite entre {0} et {1} ".format(self.profile , self.Autre_utilisateur)







"""
    class Destinataire :
        Destinataires des pétitions
        Champs :
            .nom
            .prenom
            .fonction
"""
#class Destinataire(object):

