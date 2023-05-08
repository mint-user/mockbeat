# Generated by Django 4.2.1 on 2023-05-08 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_api', '0008_schema_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='script',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='marker',
            name='script',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='strategy',
            name='script_body',
            field=models.TextField(blank=True),
        ),
    ]
