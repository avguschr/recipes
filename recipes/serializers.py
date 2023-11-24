from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from recipes.models import User, Category, Recipe, Comment
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    username = CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(write_only=True, required=True, validators=[validate_password],
                         style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=256)
    allow_empty = False
    max_length = 100


class RecipeSerializer(ModelSerializer):
    level = IntegerField(min_value=1, max_value=5)
    steps = StringListField()
    ingredients = serializers.ListField(child=serializers.DictField(child=CharField(max_length=256)), allow_empty=False, max_length=100)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "user",
            "name",
            "description",
            "categories",
            "ingredients",
            "steps",
            "level",
            "date",
        )


class CommentSerializer(ModelSerializer):
    rating = IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "recipe",
            "title",
            "rating",
            "body"
        )
