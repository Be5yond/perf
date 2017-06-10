# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170523_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='detect',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\xae\x89\xe8\xa3\x85\xe5\x91\xbd\xe4\xbb\xa4'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='delete',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\x8d\xb8\xe8\xbd\xbd\xe5\x91\xbd\xe4\xbb\xa4'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='install',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\xae\x89\xe8\xa3\x85\xe5\x91\xbd\xe4\xbb\xa4'),
        ),
    ]
