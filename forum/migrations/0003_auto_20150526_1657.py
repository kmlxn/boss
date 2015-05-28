# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150524_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(to='forum.Category', null=True),
        ),
    ]
