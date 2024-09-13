# Generated by Django 5.0.7 on 2024-08-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_supplierdocuments_buyerprofile_bank_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerprofile',
            name='bank_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bank account'),
        ),
        migrations.AlterField(
            model_name='buyerprofile',
            name='electronic_wallet',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Electronic wallet'),
        ),
        migrations.AlterField(
            model_name='buyerprofile',
            name='instabuy_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instabuy account'),
        ),
        migrations.AlterField(
            model_name='buyerprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='bank_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bank account'),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='electronic_wallet',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Electronic wallet'),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='instabuy_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instabuy account'),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name'),
        ),
    ]
