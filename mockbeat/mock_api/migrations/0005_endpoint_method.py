# Generated by Django 4.2.1 on 2023-05-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0004_endpoint_url_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='method',
            field=models.CharField(choices=[], default='GET', max_length=10),
            preserve_default=False,
        ),
    ]
