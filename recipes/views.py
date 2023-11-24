from knox.auth import TokenAuthentication
from rest_framework import status, permissions, serializers
from rest_framework.generics import CreateAPIView, get_object_or_404
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

from recipes.models import User, Recipe, Category, Comment
from recipes.serializers import UserSerializer, RecipeSerializer, CommentSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class RegisterView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class RecipeView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecipeSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category")

        if category is not None:
            recipes = Recipe.objects.filter(categories__name=category)
            return recipes
        else:
            recipes = Recipe.objects.all()

        return recipes

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # if serializer.is_valid():
        #     return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.id
        new_recipe = Recipe.objects.create(
            name=data["name"],
            description=data["description"],
            level=data["level"],
            ingredients=data["ingredients"],
            user=self.request.user,
            steps=data["steps"]
        )

        for cat in data["categories"]:
            cat_obj = Category.objects.get(id=cat["id"])
            new_recipe.categories.add(cat_obj)

        serializer = RecipeSerializer(new_recipe, data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        recipe = self.request.query_params.get("recipe")

        if recipe is not None:
            comments = Comment.objects.filter(recipe=recipe)
            return comments
        else:
            comments = Comment.objects.all()

        return comments

    def create(self, request, *args, **kwargs):
        data = request.data
        recipes = Recipe.objects.all()
        data['user'] = self.request.user.id
        new_comment = Comment.objects.create(
            title=data["title"],
            body=data["body"],
            rating=data["rating"],
            user=self.request.user,
            recipe=get_object_or_404(recipes, pk=data["recipe"])
        )

        serializer = CommentSerializer(new_comment, data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
