# Generated by Django 4.0.6 on 2023-02-13 15:05

from django.db import migrations

def remove_self_references(apps, schema_editor):
  Tag = apps.get_model('tagforest', 'Tag')

  for tag in Tag.objects.all():
    parent = tag.parent_set.filter(name=tag.name)
    if parent:
      tag.parent_set.remove(parent.first())
    tag.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tagforest', '0015_auto_20230213_1443'),
    ]

    operations = [
        migrations.RunPython(remove_self_references, reverse_code=migrations.RunPython.noop),
    ]