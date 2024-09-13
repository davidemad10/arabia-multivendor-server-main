# Generated by Django 5.1 on 2024-08-13 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_favorite_unique_together_and_more'),
        ('product', '0014_product_review_product_alter_review_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerprofile',
            name='favorite_products',
            field=models.ManyToManyField(related_name='favorited_by', through='account.Favorite', to='product.product'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user_profile', 'product')},
        ),
    ]
