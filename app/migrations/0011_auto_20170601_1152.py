# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170531_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='command',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe5\x91\xbd\xe4\xbb\xa4'),
        ),
        migrations.AddField(
            model_name='report',
            name='log',
            field=models.TextField(default=b''),
        ),
    ]
