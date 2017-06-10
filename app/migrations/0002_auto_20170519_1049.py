# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='pid',
        ),
        migrations.AddField(
            model_name='host',
            name='pid',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
