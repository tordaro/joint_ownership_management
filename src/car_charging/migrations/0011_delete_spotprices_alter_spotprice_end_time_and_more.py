# Generated by Django 5.0.4 on 2024-05-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("car_charging", "0010_spotprice_alter_chargingsession_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SpotPrices",
        ),
        migrations.AlterField(
            model_name="spotprice",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="End time"),
        ),
        migrations.AlterField(
            model_name="spotprice",
            name="eur_pr_kwh",
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name="Price per kWh [EUR/kWh]"),
        ),
        migrations.AlterField(
            model_name="spotprice",
            name="exchange_rate",
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name="Exchange rate"),
        ),
    ]
