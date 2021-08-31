# Generated by Django 3.2.5 on 2021-07-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20210721_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='link',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
