# Generated by Django 4.0.6 on 2023-05-09 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagforest', '0025_alter_tag_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagcategory',
            name='show_in_results',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tagcategory',
            name='use_as_filter',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tree',
            name='default_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='tagforest.tagcategory'),
        ),
    ]