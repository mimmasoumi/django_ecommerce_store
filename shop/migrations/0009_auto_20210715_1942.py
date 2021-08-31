# Generated by Django 3.2.5 on 2021-07-15 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210715_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='show_slider',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='shop.category'),
        ),
    ]
