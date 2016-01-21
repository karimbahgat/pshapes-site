# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cshapes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cshapes',
            name='gweday',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cshapes',
            name='gwemonth',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cshapes',
            name='gweyear',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cshapes',
            name='gwsday',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cshapes',
            name='gwsmonth',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cshapes',
            name='gwsyear',
            field=models.FloatField(db_index=True),
        ),
    ]
