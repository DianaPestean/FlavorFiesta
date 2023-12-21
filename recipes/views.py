from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm



def recipes(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes,}
    return render(request, 'recipes/recipes.html', context)

def recipe(request, pk):
    recipeObj = Recipe.objects.get(id=pk)
    return render(request, 'recipes/single-recipe.html', {'recipe': recipeObj})


@login_required(login_url="login")
def createRecipe(request):
    form = RecipeForm()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)


@login_required(login_url="login")
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)

    if request.method == "POST":
        form = RecipeForm(request.POST,request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)


@login_required(login_url="login")
def deleteRecipe(request,pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes')
    context={'object': recipe}
    return render(request, 'bloom/delete_template.html', context)

