# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msalamaclient', '0006_auto_20150825_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccine',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/'),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='Lastupdate',
            field=models.DateField(auto_now=True),
        ),
    ]
