# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(max_length=255, blank=True)),
                ('when', models.DateTimeField()),
                ('room', models.CharField(max_length=255, choices=[(b'517A', b'517A'), (b'517B', b'517B'), (b'517C', b'517C'), (b'517D', b'517D')])),
                ('host', models.CharField(max_length=255)),
                ('talk_list', models.ForeignKey(related_name='talks', to='talks.TalkList')),
            ],
            options={
                'ordering': ('when', 'room'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='talk',
            unique_together=set([('talk_list', 'name')]),
        ),
    ]
