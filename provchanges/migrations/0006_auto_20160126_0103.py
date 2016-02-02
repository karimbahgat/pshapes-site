# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0005_auto_20160124_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='provchange',
            name='status',
            field=models.CharField(default=b'Pending', max_length=40, choices=[(b'Pending', b'Pending'), (b'Accepted', b'Accepted'), (b'NonActive', b'NonActive')]),
        ),
        migrations.AddField(
            model_name='provchange',
            name='transfer_reference',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
    ]
