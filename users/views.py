from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from .models import Profile


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created succesfully!')
            login(request, user)
            return redirect('recipes')
        else:
            messages.error(request, 'An error has occured during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('recipes')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('recipes')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out!')

    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = { 'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)
