# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 04:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0006_auto_20161009_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymember',
            name='user_field',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
