# Generated by Django 3.2.8 on 2021-11-03 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagforest', '0008_auto_20211102_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]