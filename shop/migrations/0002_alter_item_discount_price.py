# Generated by Django 3.2.5 on 2021-07-07 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
