# Generated by Django 5.2 on 2025-04-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meteo', '0007_alter_meteo_vent_direction_int_to_enum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meteo',
            name='vent_direction_int_to_enum',
            field=models.CharField(default=None, editable=False, max_length=3, null=True),
        ),
    ]
