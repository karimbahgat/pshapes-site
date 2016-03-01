# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0006_auto_20160126_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='provchange',
            name='bestversion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='provchange',
            name='changeid',
            field=models.IntegerField(null=True),
        ),
    ]
