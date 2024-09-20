# Generated by Django 5.1.1 on 2024-09-20 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_user_is_buyer_remove_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerprofile',
            name='instapay_account',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='instabuy_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instabuy account'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_buyer',
            field=models.BooleanField(default=False, verbose_name='Is Buyer'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Is Admin'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_supplier',
            field=models.BooleanField(default=False, verbose_name='Is Supplier'),
        ),
    ]
