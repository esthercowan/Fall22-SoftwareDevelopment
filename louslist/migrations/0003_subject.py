# Generated by Django 4.1.1 on 2022-10-20 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("louslist", "0002_dept_dept_url_shorthand_alter_dept_dept_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
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
                ("mnemonic", models.CharField(max_length=5)),
                ("subj_name", models.CharField(max_length=50)),
                (
                    "dept_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="louslist.dept"
                    ),
                ),
            ],
        ),
    ]
