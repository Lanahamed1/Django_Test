# Generated by Django 5.0.3 on 2024-12-18 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_review_product_alter_review_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ratings',
            new_name='reivews',
        ),
    ]
