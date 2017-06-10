# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170519_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='installed',
            field=models.CharField(default=[], max_length=255, verbose_name=b'\xe5\xb7\xb2\xe5\xae\x89\xe8\xa3\x85\xe5\xb7\xa5\xe5\x85\xb7\xe7\x8a\xb6\xe6\x80\x81'),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(unique=True, verbose_name=b'IP\xe5\x9c\xb0\xe5\x9d\x80'),
        ),
        migrations.AlterField(
            model_name='host',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='host',
            name='password',
            field=models.CharField(max_length=16, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81'),
        ),
        migrations.AlterField(
            model_name='host',
            name='user',
            field=models.CharField(max_length=16, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe6\xa8\xa1\xe7\x89\x88\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
    ]
