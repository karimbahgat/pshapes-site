# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0003_auto_20160124_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provchange',
            name='added',
            field=models.DateTimeField(),
        ),
    ]
