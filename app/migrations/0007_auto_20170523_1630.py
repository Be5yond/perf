# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170522_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\x90\x8d\xe7\xa7\xb0')),
                ('platform', models.CharField(max_length=255, verbose_name=b'\xe9\x80\x82\xe7\x94\xa8\xe7\xb3\xbb\xe7\xbb\x9f\xe5\xb9\xb3\xe5\x8f\xb0')),
                ('prefix', models.CharField(max_length=255, verbose_name=b'\xe8\xbf\x90\xe8\xa1\x8c\xe5\x91\xbd\xe4\xbb\xa4')),
                ('install', models.CharField(max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\xae\x89\xe8\xa3\x85\xe5\x91\xbd\xe4\xbb\xa4')),
                ('delete', models.CharField(max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x85\xb7\xe5\x8d\xb8\xe8\xbd\xbd\xe5\x91\xbd\xe4\xbb\xa4')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='desc',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe6\xa8\xa1\xe7\x89\x88\xe8\xaf\xb4\xe6\x98\x8e'),
        ),
        migrations.AlterField(
            model_name='host',
            name='installed',
            field=models.TextField(default=b'{"iperf": "yum\\u00a0install\\u00a0iperf && rpm -ivh epel-release-6-8.noarch.rpm", "unixbench": "yum install -y perl gcc SDL-devel mesa-libGL-devel", "speedtest": "", "fio": "yum install libaio && rpm -ivh fio-2.0.10-1.el6.rf.x86_64.rpm", "ubench": "rpm -ivh ubench-0.32-1.el6.x86_64.rpm"}', verbose_name=b'\xe5\xb7\xb2\xe5\xae\x89\xe8\xa3\x85\xe5\xb7\xa5\xe5\x85\xb7\xe7\x8a\xb6\xe6\x80\x81'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tool',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe5\xb7\xa5\xe5\x85\xb7', to='app.Tool'),
        ),
        migrations.AlterField(
            model_name='task',
            name='exec_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='task',
            name='host',
            field=models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe4\xb8\xbb\xe6\x9c\xba', to='app.Host'),
        ),
        migrations.AlterField(
            model_name='task',
            name='profile',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe6\xa8\xa1\xe7\x89\x88', to='app.Profile'),
        ),
    ]
