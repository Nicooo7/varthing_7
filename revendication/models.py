# coding: utf-8
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
    tags = models.CharField(max_length=200, null=True)
    supporter = models.ManyToManyField(User, through= "Soutien", null =True)
    champ_lexical = models.CharField (max_length = 100000, default = "vide", null = True)

    def __str__(self):
        return self.ennonce

    def nb_soutien(self):    
        soutiens = Soutien.objects.filter(propositions = self, lien = 'SO')
        i= 0
        for s in soutiens:
            i += 1
        return i

    def __nb_supporter(self):
        return Soutien.objects.filter(propositions=self).count()
    nb_supporter = property(__nb_supporter)    



    




class Lieu (models.Model):
    pays = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.pays + "__" + self.region + "__" + self.ville)

class Autre_utilisateur (models.Model):
    user = models.ForeignKey(User, null =True)

    def __str__(self):
        return "utilisateur {0} ".format (self.user)

class Evenement (models.Model):

    titre = models.CharField(max_length = 10000, null = True)
    lieu = models.CharField (max_length = 10, null = True)
    date = models.DateField (null=True)
    description = models.CharField(max_length = 10000, null = True)
    proposition = models.ForeignKey (Proposition, null=True)
    participants= models.ManyToManyField(User, through= "Soutien", null =True)
    date_creation = models.DateField (default= timezone.now, null=True)

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
    lieu = models.CharField(max_length = 200, null = True)
    theme_favoris = models.CharField(max_length = 200, null = True)
    utilisateurs_proches = models.ManyToManyField (Autre_utilisateur, through ="Proximite")
    mail = models.EmailField(max_length = 254, null = True)
    age = models.PositiveSmallIntegerField(null = True)
    sexe = models.CharField(max_length = 10, null = True)
    profession = models.CharField(max_length = 10, null = True)
    interets = models.CharField (max_length = 1000, null = True)
    date_creation = models.DateField (default= timezone.now, null=True)


    def __str__(self):
        return "profile de {0}".format(self.utilisateur)




        



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
    lieu = models.CharField(max_length=100, null = True)

    
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


class Document(models.Model):
    CHOIX_TYPE_DOCUMENT=(
        ('texte', 'texte'),
        ('article', 'article'),
        ('image', 'image'),
        ('video', 'video'),
        ('autre', 'autre')
        )
    nom = models.CharField(max_length=100)
    format= models.CharField(max_length=10, choices= CHOIX_TYPE_DOCUMENT)
    date_creation = models.DateField("Date création document", auto_now=True)
    proposition = models.ForeignKey(Proposition, null =True)
    evenement = models.ForeignKey(Evenement, null = True, blank=True)
    petition = models.ForeignKey(Petition, null = True, blank=True)
    competence = models.ForeignKey(Competence, null = True, blank=True)
    fichier = models.FileField(upload_to='uploads/%Y/%m/%d/')
    personnes= models.ManyToManyField(User, through="Soutien", null=True)

    def __str__(self):
        return self.nom

    def __createur(self):
        soutien = Soutien.objects.get(document=self, lien = 'CR')
        return soutien.user
    createur = property(__createur)

    def __nb_de_consultation(self):
        soutien = Soutien.objects.filter(document=self, lien = 'SO')
        return soutien.count()
    nb_consultations = property(__nb_de_consultation)


class Organisation (models.Model):
    description = models.CharField(max_length = 500, null = True, blank = True)
    profile = models.ForeignKey(Profile, null=True, blank = True)
    date_creation = models.DateField (default= timezone.now, null=True, blank = True)
    url_du_site = models.URLField(max_length=200, null = True, blank = True)
    nom = models.CharField(max_length = 150, null = True, blank = True)
    mail_contact =  models.EmailField(max_length=254, null= True, blank = True)
    lieu_action =  models.ManyToManyField(Lieu, blank = True)
    login = models.CharField(max_length = 20, null = True, blank = True)  
    mot_de_passe = models.CharField(max_length = 10, null = True, blank = True)
    utilisateur = models.ForeignKey(User, null=True, blank=True) 
 

    def __str__(self):
        return "organisation {0}".format(self.nom)

    def __nb_de_membre(self):
        soutien = Soutien.objects.filter(organisation=self, lien = 'SO')
        return soutien.count()
    nb_de_membre = property(__nb_de_membre)

    def __membres(self):
        return Soutien.objects.filter(organisation=self, lien = 'SO')     
    membres = property(__membres)

    def __propositions(self):
        return Proposition.objects.filter(soutien__user = self.utilisateur)     
    propositions = property(__propositions)

    def __organisations(self):
        return Organisation.objects.filter(soutien__user = self.utilisateur)     
    organisations = property(__organisations)

    def __petitions(self):
        return Petition.objects.filter(soutien__user = self.utilisateur)     
    petitions = property(__petitions)

    def __documents(self):
        return Document.objects.filter(soutien__user = self.utilisateur)     
    documents = property(__documents)

    def __evenements(self):
        return Evenement.objects.filter(soutien__user = self.utilisateur) 
    evenements = property(__evenements)

    def __competences(self):
        return Competence.objects.filter(soutien__user = self.utilisateur) 
    competences = property(__competences)




class Soutien(models.Model):

    CHOIX_LIEN= (
                ('CR' , 'createur'),
                ('SO', 'soutien'),
                
    )
    propositions = models.ForeignKey(Proposition, null =True)
    user = models.ForeignKey(User, null=True)
    lien = models.CharField(max_length =2, choices= CHOIX_LIEN)
    date = models.DateField("Date création soutien", auto_now=True)

    # Elément soutenu
    evenement = models.ForeignKey(Evenement, null = True, blank=True)
    petition = models.ForeignKey(Petition, null = True, blank=True)
    competence = models.ForeignKey(Competence, null = True, blank=True)
    document= models.ForeignKey(Document, null = True, blank=True)
    organisation= models.ForeignKey(Organisation, null = True, blank= True)
   


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

