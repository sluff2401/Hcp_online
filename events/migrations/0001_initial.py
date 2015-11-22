# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='E',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('e_date', models.DateField()),
                ('detail_public', models.TextField(null=True, blank=True)),
                ('detail_private', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_live', models.BooleanField(default=True)),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='bookedin')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='author')),
            ],
        ),
    ]
