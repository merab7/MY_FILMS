# Generated by Django 5.0.3 on 2024-03-15 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_myt_10_description_text_of_t10_myt_10_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myt_10',
            name='id',
        ),
        migrations.AlterField(
            model_name='myt_10',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='blog.filmcard'),
        ),
    ]
