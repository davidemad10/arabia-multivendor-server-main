# Generated by Django 5.1.1 on 2024-10-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
