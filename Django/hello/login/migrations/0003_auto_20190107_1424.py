# Generated by Django 2.1.4 on 2019-01-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190107_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_input', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='logon',
            name='logging_in',
            field=models.CharField(default='SOME STRING', max_length=20),
        ),
    ]
