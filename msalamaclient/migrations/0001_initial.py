# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstchoicedate', models.DateTimeField()),
                ('secondchoicedate', models.DateTimeField()),
                ('purposeofvisit', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messagefrom', models.CharField(max_length=150)),
                ('messageto', models.CharField(max_length=150)),
                ('message', models.CharField(max_length=800)),
                ('messagesubject', models.CharField(max_length=100, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageSent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=800)),
                ('messagesubject', models.CharField(max_length=100, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientVaccination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('dateofvaccinereceiption', models.DateField()),
                ('locationofreception', models.CharField(max_length=150, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SideEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaint', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateofbirth', models.DateField()),
                ('height', models.CharField(max_length=200)),
                ('weight', models.CharField(max_length=200)),
                ('IDNum', models.CharField(max_length=200)),
                ('Residence', models.CharField(max_length=200)),
                ('PhoneNum', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vaccinename', models.CharField(max_length=200)),
                ('vaccineIDnum', models.CharField(max_length=150)),
                ('vaccineEdition', models.CharField(max_length=150)),
                ('aboutVaccine', models.CharField(max_length=500)),
                ('Lastupdate', models.DateField(auto_now=True)),
                ('vaccineDoseCount', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=b'images/')),
                ('childVaccine', models.BooleanField(default=True, verbose_name=True)),
            ],
        ),
        migrations.CreateModel(
            name='VaccineDose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vaccinedose', models.CharField(max_length=150)),
                ('vaccinedoseday', models.IntegerField()),
                ('available', models.BooleanField()),
                ('vaccine', models.ForeignKey(to='msalamaclient.Vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='vaccineSideEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sideEffectDesc', models.CharField(max_length=80)),
                ('vaccine', models.ForeignKey(to='msalamaclient.Vaccine')),
            ],
        ),
        migrations.AddField(
            model_name='sideeffect',
            name='patient',
            field=models.ForeignKey(to='msalamaclient.UserProfile'),
        ),
        migrations.AddField(
            model_name='sideeffect',
            name='vaccine',
            field=models.ForeignKey(to='msalamaclient.Vaccine'),
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='patient',
            field=models.ForeignKey(to='msalamaclient.UserProfile'),
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='patient_vaccine',
            field=models.ForeignKey(to='msalamaclient.Vaccine'),
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='vaccinedose',
            field=models.ForeignKey(to='msalamaclient.VaccineDose'),
        ),
        migrations.AddField(
            model_name='messagesent',
            name='patient',
            field=models.ForeignKey(to='msalamaclient.UserProfile'),
        ),
        migrations.AddField(
            model_name='message',
            name='patient',
            field=models.ForeignKey(to='msalamaclient.UserProfile'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='msalamaclient.UserProfile'),
        ),
    ]
