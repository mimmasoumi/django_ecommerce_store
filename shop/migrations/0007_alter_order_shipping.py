# Generated by Django 3.2.5 on 2021-07-11 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210711_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shipping'),
        ),
    ]
