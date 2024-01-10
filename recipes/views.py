from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe, Tag
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, ReviewForm
from django.contrib import messages
from .utils import searchRecipes, paginateRecipes


def recipes(request):
    recipes, search_query = searchRecipes(request)
    custom_range, recipes = paginateRecipes(request, recipes, 6)

    context = {'recipes': recipes, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'recipes/recipes.html', context)

@login_required(login_url="login")
def createRecipe(request):
    profile = request.user.profile
    form = RecipeForm()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = profile
            recipe.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)


def recipe(request, pk):
    recipeObj = Recipe.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.recipe = recipeObj
        review.owner = request.user.profile
        review.save()

        recipeObj.getVoteCount

        messages.success(request, 'Thank you for your review!')
        return redirect('recipe', pk=recipeObj.id)

    return render(request, 'recipes/single-recipe.html', {'recipe': recipeObj, 'form': form})

@login_required(login_url="login")
def updateRecipe(request, pk):
    profile = request.user.profile
    recipe = profile.recipe_set.get(id=pk)
    form = RecipeForm(instance=recipe)

    if request.method == "POST":
        form = RecipeForm(request.POST,request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'recipes/recipe_form.html', context)


@login_required(login_url="login")
def deleteRecipe(request,pk):
    profile = request.user.profile
    recipe = profile.recipe_set.get(id=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes')
    context={'object': recipe}
    return render(request, 'delete_template.html', context)

