# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='tab_name',
            field=models.CharField(max_length=64, verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe8\xa1\xa8\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
    ]
