from django.contrib import admin

# Register your models here.
from .models import Recipe, Review, Tag

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Tag)