from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .form import CustomUserCreationForm, ProfileEditForm,SkillForm,MessageForm
from django.contrib import messages
from .models import Profile,Message
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles,paginatorProfiles


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range,profiles = paginatorProfiles(request,profiles,10)
    context = {
        'profiles': profiles,
        'search_query':search_query,
        'custom_range':custom_range,
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
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'user_account')
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

@login_required(login_url="login_user")
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

@login_required(login_url="login_user")
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


@login_required(login_url="login_user")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadMessage = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests':messageRequests,
        'unreadMessage':unreadMessage
    }
    return render(request,'inbox.html',context)

@login_required(login_url="login_user")
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context ={
        'message':message,
    }
    return render(request,'messageView.html',context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request,'Your Message Successfully Send  !')
            return redirect('user-profile',pk=recipient.id)

    context= {
        'recipient':recipient,
        'form':form,
    }
    return render(request, 'message_form.html',context)