# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0002_auto_20150816_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='slug',
            field=models.SlugField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='talk',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
