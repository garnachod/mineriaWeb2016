# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=20)),
                ('idioma', models.CharField(max_length=2)),
                ('inicio', models.DateTimeField()),
            ],
        ),
    ]