# Generated by Django 5.1.9 on 2025-05-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meteo', '0010_meteo_display_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meteo',
            name='display_order',
        ),
        migrations.AddField(
            model_name='spot',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
    ]
