# Generated by Django 5.1.6 on 2025-02-20 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesa_transactions',
            name='timestamp',
            field=models.IntegerField(null=True),
        ),
    ]
