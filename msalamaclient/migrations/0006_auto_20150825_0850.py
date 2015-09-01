# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0005_vaccine_childvaccine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccine',
            name='aboutVaccine',
            field=models.CharField(max_length=500),
        ),
    ]
