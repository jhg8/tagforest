from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tree, Tag, TagCategory, Graph

@receiver(post_save, sender=User)
def create_default_tree(sender, **kwargs):
    user = kwargs.get('instance')
    if not Tree.objects.filter(user=user):
      Tree.objects.create(name="Default", user=user)
