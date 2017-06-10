# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170519_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField(default=None, null=True, blank=True)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(to='app.Task')),
            ],
        ),
        migrations.RemoveField(
            model_name='host',
            name='pid',
        ),
    ]
