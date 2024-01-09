from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('recipe/<str:pk>/', views.recipe, name='recipe'),
    path('add-recipe/', views.createRecipe, name='add-recipe'),
    path('update-recipe/<str:pk>/', views.updateRecipe, name='update-recipe'),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name='delete-recipe')
]