# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-28 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provshapes', '0007_auto_20171228_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provshape',
            name='simplify',
            field=models.FloatField(db_index=True, null=True),
        ),
    ]
