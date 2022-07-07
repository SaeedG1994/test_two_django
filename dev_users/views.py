from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .form import CustomUserCreationForm, ProfileEditForm,SkillForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles


def profiles(request):
    profiles, search_query = searchProfiles(request)
    context = {
        'profiles': profiles,
        'search_query':search_query,
    }
    return render(request, 'All-profile.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkill': topSkill,
        'otherSkill': otherSkill
    }
    return render(request, 'user-Profile.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'username or password is incorrect')
    return render(request, 'login_register.html')


def logOutUser(request):
    logout(request)
    messages.info(request, 'logOuting is successfully')
    return redirect('login_user')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created. Please Confirm your Information')
            login(request, user)
            return redirect('edit_profile')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'login_register.html', context)


@login_required(login_url='login_user')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'account_User.html', context)


@login_required(login_url='login_user')
def editProfile(request):
    profile = request.user.profile
    form = ProfileEditForm(instance=profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Profile Has Been Updated')
            return redirect('user_account')
    context = {
        'form': form
    }
    return render(request, 'edit-profile.html', context)


@login_required(login_url="login_user")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner =profile
            skill.save()
            messages.success(request,'Skill Created Successfully 😊')
            return redirect('user_account')
    context ={
        'form':form,

    }
    return render(request,'create_Skill_Form.html',context)


def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was Updated 😎')
            return redirect('user_account')

    context = {
        'form':form
    }
    return render(request,'create_Skill_Form.html',context)


def deleteSkill(request,pk):
    profile = request.user.profile
    skill =profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was successfully Deleted 😒')
        return redirect('user_account')
    context ={
        'object':skill
    }
    return render(request,'delete_form.html',context)