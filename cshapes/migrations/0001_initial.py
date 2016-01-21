# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cshapes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sp_id', models.CharField(max_length=5)),
                ('cntry_name', models.CharField(max_length=30)),
                ('area', models.FloatField()),
                ('capname', models.CharField(max_length=19)),
                ('caplong', models.FloatField()),
                ('caplat', models.FloatField()),
                ('featureid', models.IntegerField()),
                ('cowcode', models.IntegerField()),
                ('cowsyear', models.IntegerField()),
                ('cowsmonth', models.IntegerField()),
                ('cowsday', models.IntegerField()),
                ('coweyear', models.IntegerField()),
                ('cowemonth', models.IntegerField()),
                ('coweday', models.IntegerField()),
                ('gwcode', models.IntegerField()),
                ('gwsyear', models.FloatField()),
                ('gwsmonth', models.FloatField()),
                ('gwsday', models.FloatField()),
                ('gweyear', models.FloatField()),
                ('gwemonth', models.FloatField()),
                ('gweday', models.FloatField()),
                ('isoname', models.CharField(max_length=42)),
                ('iso1num', models.IntegerField()),
                ('iso1al2', models.CharField(max_length=7)),
                ('iso1al3', models.CharField(max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=-1)),
            ],
        ),
    ]
