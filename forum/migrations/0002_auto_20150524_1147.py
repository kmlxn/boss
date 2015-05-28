# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', null=True),
        ),
    ]
