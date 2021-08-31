# Generated by Django 3.2.5 on 2021-07-16 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.item'),
            preserve_default=False,
        ),
    ]