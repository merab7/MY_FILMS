# Generated by Django 5.0.3 on 2024-03-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_myt_10_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myt_10',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]