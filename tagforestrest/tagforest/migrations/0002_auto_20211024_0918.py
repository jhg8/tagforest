# Generated by Django 3.2.8 on 2021-10-24 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tagforest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='tree',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tree',
        ),
        migrations.DeleteModel(
            name='Tree',
        ),
    ]
