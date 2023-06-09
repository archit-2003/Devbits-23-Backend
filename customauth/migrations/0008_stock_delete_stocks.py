# Generated by Django 4.1.7 on 2023-04-01 06:59

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("customauth", "0007_stocks"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock_name", models.CharField(default="Bitcoin", max_length=100)),
                ("stock_originalprice", models.IntegerField(default=0)),
                ("stock_time", models.CharField(default="13:44:34", max_length=100)),
                ("stock_date", models.CharField(default="12-01-2022", max_length=100)),
                (
                    "stock_user_email",
                    models.EmailField(
                        default="a@gmail.com",
                        max_length=60,
                        null=True,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="Email",
                    ),
                ),
                ("cnt", models.IntegerField(default=0)),
                ("password", models.TimeField(default=django.utils.timezone.now)),
                ("stock_status", models.CharField(default="Cart", max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="Stocks",
        ),
    ]
