# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SideEffectbyVaccine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sideEffectDesc', models.CharField(max_length=80)),
                ('vaccine', models.ForeignKey(to='msalamaclient.Vaccine')),
            ],
        ),
        migrations.RemoveField(
            model_name='vaccinesideeffect',
            name='vaccine',
        ),
        migrations.DeleteModel(
            name='vaccineSideEffect',
        ),
    ]
