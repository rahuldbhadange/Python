# Generated by Django 2.1.4 on 2019-01-07 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Password',
        ),
        migrations.RemoveField(
            model_name='logon',
            name='logging_in',
        ),
    ]
