from django.contrib import admin

from .models import Category, Item, Request

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Request)