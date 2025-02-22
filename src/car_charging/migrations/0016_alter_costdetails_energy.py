# Generated by Django 5.0.6 on 2025-01-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("car_charging", "0015_alter_energydetails_energy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="costdetails",
            name="energy",
            field=models.DecimalField(decimal_places=6, editable=False, max_digits=10, verbose_name="Energy [kWh]"),
        ),
    ]
