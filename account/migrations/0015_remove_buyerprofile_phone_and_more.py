# Generated by Django 5.1.1 on 2024-10-10 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='supplierprofile',
            name='phone',
        ),
    ]
