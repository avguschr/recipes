from django.contrib import admin
from recipes.models import User, Category, Recipe, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)
