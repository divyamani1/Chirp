# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='profile_photos')),
            ],
        ),
    ]
