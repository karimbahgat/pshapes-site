# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0002_auto_20160123_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='provchange',
            name='added',
            field=models.DateTimeField(default=datetime.date(2016, 1, 24), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provchange',
            name='user',
            field=models.CharField(default='kimo', max_length=200),
            preserve_default=False,
        ),
    ]
