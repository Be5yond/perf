# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170522_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='installed',
            field=models.CharField(default=b'{"iperf": "yum\\u00a0install\\u00a0iperf && rpm -ivh epel-release-6-8.noarch.rpm", "unixbench": "yum install -y perl gcc SDL-devel mesa-libGL-devel", "fio": "yum install libaio && rpm -ivh fio-2.0.10-1.el6.rf.x86_64.rpm", "ubench": "rpm -ivh ubench-0.32-1.el6.x86_64.rpm"}', max_length=255, verbose_name=b'\xe5\xb7\xb2\xe5\xae\x89\xe8\xa3\x85\xe5\xb7\xa5\xe5\x85\xb7\xe7\x8a\xb6\xe6\x80\x81'),
        ),
    ]
