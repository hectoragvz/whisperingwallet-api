# Generated by Django 5.0.4 on 2024-04-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="total",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]