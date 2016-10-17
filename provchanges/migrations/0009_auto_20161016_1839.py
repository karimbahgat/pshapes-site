# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0008_auto_20160314_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provchange',
            name='country',
        ),
        migrations.AddField(
            model_name='provchange',
            name='fromalterns',
            field=models.CharField(max_length=40, verbose_name='From alternate province names', blank=True),
        ),
        migrations.AddField(
            model_name='provchange',
            name='fromcapitalname',
            field=models.CharField(max_length=40, verbose_name='From province capital (name change)', blank=True),
        ),
        migrations.AddField(
            model_name='provchange',
            name='fromcountry',
            field=models.CharField(default='default', max_length=40, verbose_name='From country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provchange',
            name='toalterns',
            field=models.CharField(max_length=40, verbose_name='To province alternate names', blank=True),
        ),
        migrations.AddField(
            model_name='provchange',
            name='tocapitalname',
            field=models.CharField(max_length=40, verbose_name='To province capital (name change)', blank=True),
        ),
        migrations.AddField(
            model_name='provchange',
            name='tocountry',
            field=models.CharField(default='default', max_length=40, verbose_name='To country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='provchange',
            name='date',
            field=models.DateField(verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromcapital',
            field=models.CharField(max_length=40, verbose_name='From province capital (moved)', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromfips',
            field=models.CharField(max_length=40, verbose_name='From province FIPS code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromhasc',
            field=models.CharField(max_length=40, verbose_name='From province HASC code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromiso',
            field=models.CharField(max_length=40, verbose_name='From province ISO code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromname',
            field=models.CharField(max_length=40, verbose_name='From province name'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='fromtype',
            field=models.CharField(blank=True, max_length=40, verbose_name='From province type', choices=[(b'Province', b'Province'), (b'Municipality', b'Municipality'), (b'District', b'District'), (b'County', b'County'), (b'State', b'State'), (b'Parish', b'Parish'), (b'Region', b'Region'), (b'Prefecture', b'Prefecture'), (b'Department', b'Department'), (b'Governate', b'Governate'), (b'Other...', b'Other...')]),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='source',
            field=models.CharField(max_length=400, verbose_name='Source of information'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='tocapital',
            field=models.CharField(max_length=40, verbose_name='To province capital (moved)', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='tofips',
            field=models.CharField(max_length=40, verbose_name='To province FIPS code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='tohasc',
            field=models.CharField(max_length=40, verbose_name='To province HASC code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='toiso',
            field=models.CharField(max_length=40, verbose_name='To province ISO code', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='toname',
            field=models.CharField(max_length=40, verbose_name='To province name'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='totype',
            field=models.CharField(blank=True, max_length=40, verbose_name='To province type', choices=[(b'Province', b'Province'), (b'Municipality', b'Municipality'), (b'District', b'District'), (b'County', b'County'), (b'State', b'State'), (b'Parish', b'Parish'), (b'Region', b'Region'), (b'Prefecture', b'Prefecture'), (b'Department', b'Department'), (b'Governate', b'Governate'), (b'Other...', b'Other...')]),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='transfer_geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, verbose_name='Province geometry', blank=True),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='transfer_reference',
            field=models.CharField(max_length=400, verbose_name='Map description'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='transfer_source',
            field=models.CharField(max_length=200, verbose_name='Link to map data'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='type',
            field=models.CharField(max_length=40, verbose_name='Type of Change', choices=[(b'NewInfo', b'NewInfo'), (b'PartTransfer', b'PartTransfer'), (b'FullTransfer', b'FullTransfer'), (b'Breakaway', b'Breakaway')]),
        ),
    ]
