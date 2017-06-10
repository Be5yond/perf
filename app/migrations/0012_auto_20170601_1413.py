# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170601_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='pid',
        ),
        migrations.AddField(
            model_name='report',
            name='tid',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
