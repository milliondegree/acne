# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-01 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myacne', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='Icontext',
        ),
    ]