# Generated by Django 5.0.3 on 2024-03-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_post_is_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]