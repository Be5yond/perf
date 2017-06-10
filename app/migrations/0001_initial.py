# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'init', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'init', b'init'), (b'installing', b'installing'), (b'idle', b'idle'), (b'errortesting', b'errortesting'), (b'offline', b'offline')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('name', models.CharField(max_length=255)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('info', models.TextField(default=b'')),
                ('user', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('tool', models.CharField(max_length=64, verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe5\xb7\xa5\xe5\x85\xb7')),
                ('params', models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\x91\xbd\xe4\xbb\xa4\xe5\x8f\x82\xe6\x95\xb0')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'wait', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'wait', b'wait'), (b'running', b'running'), (b'finish', b'finish')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('exec_time', models.DateTimeField(auto_now_add=True)),
                ('result', models.CharField(default=b'', max_length=16)),
                ('log', models.TextField(default=b'')),
                ('pid', models.IntegerField(default=None, null=True, blank=True)),
                ('host', models.ForeignKey(to='app.Host')),
                ('profile', models.ForeignKey(to='app.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
