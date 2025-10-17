from django.contrib import admin
from .models import Status, Type, Category, SubCategory, Transaction

# This tells Django to create an admin interface for each of your models.
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Transaction)
