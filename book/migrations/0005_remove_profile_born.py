# Generated by Django 3.0.5 on 2020-04-18 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='born',
        ),
    ]