# Generated by Django 3.2.9 on 2023-01-26 22:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_trial',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='trial_ends_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
