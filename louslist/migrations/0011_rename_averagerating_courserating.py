# Generated by Django 4.1.1 on 2022-11-13 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("louslist", "0010_alter_averagerating_course_num"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="AverageRating",
            new_name="CourseRating",
        ),
    ]