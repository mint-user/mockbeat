# Generated by Django 4.2.1 on 2023-05-07 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0005_endpoint_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='method',
            field=models.CharField(choices=[('CONNECT', 'Connect'), ('DELETE', 'Delete'), ('GET', 'Get'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('PATCH', 'Patch'), ('POST', 'Post'), ('PUT', 'Put'), ('TRACE', 'Trace')], max_length=10),
        ),
    ]