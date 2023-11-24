from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=128, null=False, blank=False, unique=True)
    img = models.ImageField(upload_to='static/images/', null=True, max_length=300)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Recipe(models.Model):
    name = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    img = models.ImageField(upload_to='static/images/', null=True, max_length=300)
    steps = models.JSONField(default=list)
    ingredients = models.JSONField(default=dict)
    level = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    categories = models.ManyToManyField(Category, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, max_length=128, blank=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, max_length=128, blank=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, max_length=128, blank=False)
    title = models.CharField(max_length=256, null=False)
    rating = models.IntegerField()
    body = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=False)

    def __str__(self):
        return self.title
