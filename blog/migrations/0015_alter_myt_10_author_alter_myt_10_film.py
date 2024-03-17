# Generated by Django 5.0.3 on 2024-03-17 14:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_myt_10_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='myt_10',
            name='author',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='myt_10',
            name='film',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.filmcard'),
        ),
    ]