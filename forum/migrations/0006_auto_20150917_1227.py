# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_topic_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.ImageField(null=True, blank=True, upload_to='images'),
        ),
    ]
