from django.contrib import admin
from .models import Tag, TagCategory, Tree

# Register your models here.
admin.site.register(Tag)
admin.site.register(TagCategory)
admin.site.register(Tree)
