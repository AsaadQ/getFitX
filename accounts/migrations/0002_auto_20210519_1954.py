# Generated by Django 3.1.7 on 2021-05-19 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profil',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
