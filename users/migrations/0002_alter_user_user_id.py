# Generated by Django 3.2.8 on 2021-12-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False),
        ),
    ]
