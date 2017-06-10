# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170524_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='installed',
        ),
    ]
