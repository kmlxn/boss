# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20150526_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='downvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topic',
            name='downvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topic',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
    ]
