# Generated by Django 4.1.1 on 2022-12-02 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("louslist", "0013_rating_user_rates_once_per_course"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("comment", models.TextField()),
            ],
        ),
    ]
