# Generated by Django 4.2.1 on 2023-05-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0006_alter_endpoint_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='url_part',
            field=models.CharField(default='', max_length=100),
        ),
    ]
