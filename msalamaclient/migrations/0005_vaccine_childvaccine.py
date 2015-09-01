# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0004_auto_20150825_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccine',
            name='childVaccine',
            field=models.BooleanField(default=True, verbose_name=True),
            preserve_default=False,
        ),
    ]
