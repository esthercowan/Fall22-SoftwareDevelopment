# Generated by Django 4.1.2 on 2022-11-02 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("louslist", "0004_merge_0002_search_0003_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="rating",
            field=models.IntegerField(default=0),
        ),
    ]