# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('hash_id', models.CharField(blank=True, max_length=128, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Modified')),
                ('content', models.TextField(max_length='5242880')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pastes', to='profiles.Profile')),
            ],
        ),
    ]