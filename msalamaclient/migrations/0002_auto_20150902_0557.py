# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccine',
            name='childVaccine',
            field=models.BooleanField(default=True),
        ),
    ]
