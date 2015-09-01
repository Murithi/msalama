# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0002_auto_20150824_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinedose',
            name='vaccinedoseday',
            field=models.CharField(max_length=100),
        ),
    ]
