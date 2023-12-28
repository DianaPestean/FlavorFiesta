from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, SkillForm,ProfileForm, MessageForm  #WE HAVE FORMS TO ADD HERE
from django.contrib.auth.models import User
from .models import Profile, Message
from django.core.mail import send_mail,EmailMultiAlternatives # for emails
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import searchProfiles, paginateProfiles
from django.contrib.auth.decorators import login_required
from django.urls import conf
from django.db.models import Q



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

        ### welcoming email
            my_subject = "🌮 Welcome to Flavor Fiesta !"
            my_recipient = form.cleaned_data['email']
            user.username = user.username.capitalize()
            welcome_user = f"{user.username}"
            link_app = "http://127.0.0.1:8000"
            context = {
                "welcome_user": welcome_user,
                "link_app": link_app
            }
            html_message = render_to_string('registration/email_welcome_message.html', context=context)
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject=my_subject,
                body=plain_message,
                from_email=None,
                to=[my_recipient],
            )
            message.attach_alternative(html_message, "text/html")
            message.send()
        ### welcoming email


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
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'recipes')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out!')

    return redirect('login')


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)
    

    context = { 'profiles': profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

# All done until here
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    recipes = profile.recipe_set.all()

    context = {'profile': profile, 'skills': skills, 'recipes': recipes}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance= profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')


    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')


    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url="login")
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context={'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    # We can add a date_read attribute to the Message class in models and modify it here
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email 
                
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('user-profile', pk=recipient.id)

    context={'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)
