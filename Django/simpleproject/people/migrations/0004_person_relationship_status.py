# Generated by Django 2.1.4 on 2019-01-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20190110_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='relationship_status',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
