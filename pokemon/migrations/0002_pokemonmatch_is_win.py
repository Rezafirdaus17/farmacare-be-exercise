# Generated by Django 3.2.16 on 2022-12-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemonmatch",
            name="is_win",
            field=models.BooleanField(default=False),
        ),
    ]