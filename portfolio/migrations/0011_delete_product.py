# Generated by Django 3.1.13 on 2021-07-15 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_product_friendly_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
