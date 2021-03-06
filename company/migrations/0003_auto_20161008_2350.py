# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 17:50
from __future__ import unicode_literals

import company.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_companymember_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymember',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='companymember',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='companymember',
            name='photo',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=company.models.upload_location, width_field='width_field'),
        ),
    ]
