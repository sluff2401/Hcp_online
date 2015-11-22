# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_private',
            field=models.TextField(null=True, blank=True, verbose_name='Details to be shown only to logged in users'),
        ),
        migrations.AlterField(
            model_name='e',
            name='detail_public',
            field=models.TextField(null=True, blank=True, verbose_name='Details to be shown publicly'),
        ),
        migrations.AlterField(
            model_name='e',
            name='e_date',
            field=models.DateField(verbose_name='Date of the event, in the format "yyyy-mm-dd", e.g. for 31st December 2015, enter "2015-12-31"'),
        ),
    ]
