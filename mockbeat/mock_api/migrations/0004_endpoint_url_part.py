# Generated by Django 4.2 on 2023-05-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0003_rename_base_url_endpoint_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='url_part',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]