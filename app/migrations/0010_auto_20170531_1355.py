# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_host_installed'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='suffix',
            field=models.CharField(default='', max_length=255, verbose_name=b'\xe8\xbf\x90\xe8\xa1\x8c\xe5\x91\xbd\xe4\xbb\xa4\xe5\x90\x8e\xe7\xbc\x80'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='host',
            name='status',
            field=model_utils.fields.StatusField(default=b'idle', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
    ]
