# Generated by Django 4.2 on 2023-05-06 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0002_alter_endpoint_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endpoint',
            old_name='base_url',
            new_name='url',
        ),
    ]
