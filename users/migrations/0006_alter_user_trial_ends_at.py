# Generated by Django 4.1.6 on 2023-02-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_delete_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='trial_ends_at',
            field=models.DateTimeField(null=True),
        ),
    ]
