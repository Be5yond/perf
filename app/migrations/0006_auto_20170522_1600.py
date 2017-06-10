# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170522_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='desc',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe6\x8f\x8f\xe8\xbf\xb0'),
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe6\xa8\xa1\xe7\x89\x88\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
    ]
