# Generated by Django 3.2.4 on 2025-02-06 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_generic',
        ),
    ]
