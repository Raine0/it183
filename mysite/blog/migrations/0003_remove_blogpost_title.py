# Generated by Django 5.0 on 2024-11-17 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='title',
        ),
    ]