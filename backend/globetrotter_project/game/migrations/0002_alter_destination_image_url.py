# Generated by Django 4.2 on 2025-03-03 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
