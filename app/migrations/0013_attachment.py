# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170601_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6\xe5\x90\x8d\xe7\xa7\xb0')),
                ('url', models.CharField(default=b'', max_length=255, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80')),
                ('tab_name', models.IntegerField(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe8\xa1\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('tab_id', models.IntegerField(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe8\xa1\xa8id')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
