"""
URL configuration for recipes_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from recipes.views import RegisterView, LoginView, RecipeView, CommentView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("recipe/", RecipeView.as_view({'get': 'list', 'post': 'create'}), name="create_recipe"),
    path("recipe/<int:pk>/", RecipeView.as_view({'get': 'retrieve', 'patch': 'update'}), name="recipe"),
    path("comment/", CommentView.as_view({'get': 'list', 'post': 'create'}))
]