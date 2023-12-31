# Generated by Django 4.1.11 on 2023-12-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalmSongs",
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
                ("title", models.TextField()),
                ("artist", models.TextField()),
                ("image", models.ImageField(upload_to="")),
                ("audio_file", models.FileField(blank=True, null=True, upload_to="")),
                ("audio_link", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="HappySongs",
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
                ("title", models.TextField()),
                ("artist", models.TextField()),
                ("image", models.ImageField(upload_to="")),
                ("audio_file", models.FileField(blank=True, null=True, upload_to="")),
                ("audio_link", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="MotivationalSongs",
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
                ("title", models.TextField()),
                ("artist", models.TextField()),
                ("image", models.ImageField(upload_to="")),
                ("audio_file", models.FileField(blank=True, null=True, upload_to="")),
                ("audio_link", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="SadSongs",
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
                ("title", models.TextField()),
                ("artist", models.TextField()),
                ("image", models.ImageField(upload_to="")),
                ("audio_file", models.FileField(blank=True, null=True, upload_to="")),
                ("audio_link", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
