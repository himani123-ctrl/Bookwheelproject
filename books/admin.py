from django.contrib import admin
from .models import Author, Story, Category

admin.site.register(Author)
admin.site.register(Story)
admin.site.register(Category)
