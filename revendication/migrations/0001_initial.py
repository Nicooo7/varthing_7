# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-28 10:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autre_utilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField(verbose_name='Descrition de la compétence recherchée')),
                ('date_creation', models.DateField(auto_now=True, verbose_name='Date de création')),
                ('date_echeance', models.DateField(blank=True, null=True, verbose_name="Date d'échéance")),
                ('lieu', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('format', models.CharField(choices=[('texte', 'texte'), ('article', 'article'), ('image', 'image'), ('video', 'video'), ('autre', 'autre')], max_length=10)),
                ('date_creation', models.DateField(auto_now=True, verbose_name='Date création document')),
                ('fichier', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('competence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Competence')),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=10000, null=True)),
                ('lieu', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(null=True)),
                ('description', models.CharField(max_length=10000, null=True)),
                ('date_creation', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('ville', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('date_creation', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('url_du_site', models.URLField(blank=True, null=True)),
                ('nom', models.CharField(blank=True, max_length=150, null=True)),
                ('mail_contact', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField(verbose_name='Descrition de la pétition')),
                ('date_creation', models.DateField(auto_now=True, verbose_name='Date de création')),
                ('date_echeance', models.DateField(blank=True, null=True, verbose_name="Date d'échéance")),
                ('objectif_de_signataires', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu', models.CharField(max_length=200, null=True)),
                ('theme_favoris', models.CharField(max_length=200, null=True)),
                ('mail', models.EmailField(max_length=254, null=True)),
                ('age', models.PositiveSmallIntegerField(null=True)),
                ('sexe', models.CharField(max_length=10, null=True)),
                ('profession', models.CharField(max_length=10, null=True)),
                ('interets', models.CharField(max_length=1000, null=True)),
                ('date_creation', models.DateField(default=django.utils.timezone.now, null=True)),
                ('utilisateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ennonce', models.CharField(max_length=200, null=True)),
                ('date_creation', models.DateField(default=django.utils.timezone.now, null=True)),
                ('tags', models.CharField(max_length=200, null=True)),
                ('champ_lexical', models.CharField(default='vide', max_length=100000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proximite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proba', models.DecimalField(decimal_places=3, max_digits=5)),
                ('Autre_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='revendication.Autre_utilisateur')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Soutien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lien', models.CharField(choices=[('CR', 'createur'), ('SO', 'soutien')], max_length=2)),
                ('date', models.DateField(auto_now=True, verbose_name='Date création soutien')),
                ('competence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Competence')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Document')),
                ('evenement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Evenement')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Organisation')),
                ('petition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Petition')),
                ('propositions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Proposition')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='proposition',
            name='supporter',
            field=models.ManyToManyField(null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='utilisateurs_proches',
            field=models.ManyToManyField(through='revendication.Proximite', to='revendication.Autre_utilisateur'),
        ),
        migrations.AddField(
            model_name='petition',
            name='propositions',
            field=models.ManyToManyField(null=True, to='revendication.Proposition'),
        ),
        migrations.AddField(
            model_name='petition',
            name='signataires',
            field=models.ManyToManyField(null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisation',
            name='membres',
            field=models.ManyToManyField(blank=True, null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisation',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Profile'),
        ),
        migrations.AddField(
            model_name='evenement',
            name='participants',
            field=models.ManyToManyField(null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evenement',
            name='proposition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Proposition'),
        ),
        migrations.AddField(
            model_name='document',
            name='evenement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Evenement'),
        ),
        migrations.AddField(
            model_name='document',
            name='personnes',
            field=models.ManyToManyField(null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='petition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Petition'),
        ),
        migrations.AddField(
            model_name='document',
            name='proposition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='revendication.Proposition'),
        ),
        migrations.AddField(
            model_name='competence',
            name='personnes',
            field=models.ManyToManyField(null=True, through='revendication.Soutien', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='competence',
            name='propositions',
            field=models.ManyToManyField(null=True, to='revendication.Proposition'),
        ),
    ]
