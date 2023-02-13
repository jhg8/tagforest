from django.contrib import admin
from .models import Tag, TagCategory

# Register your models here.
admin.site.register(Tag)
admin.site.register(TagCategory)
