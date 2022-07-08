from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import ProjectForm
from .models import Project,Tag
from .utils import projectSearch,paginationProjects


def projects(request):
    projects,search_query = projectSearch(request)
    custom_range ,projects =paginationProjects(request,projects,6)
    context = {'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects.html',context)


def single_project(request,pk):
    project = Project.objects.get(id=pk)
    tag = project.tags.all()
    context = {
        'project':project,
        'tag': tag,
    }
    return render(request,'single-project.html',context)

@login_required(login_url="login_user")
def update_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form =ProjectForm(instance=project)
    if request.method == 'POST':
        form =ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context ={
        'project':project,
        'form':form
    }
    return render(request, 'project_form.html', context)

@login_required(login_url="login_user")
def delete_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request,'Your Project Successfully Deleted!')
        return  redirect('user_account')
    context = {
        'project':project
    }
    return render(request, 'delete_form.html', context)

@login_required(login_url="login_user")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            messages.success(request,'Your Project Created Successfully 😍')
            return redirect('user_account')
    context ={
        'form':form
    }
    return render(request, 'project_form.html', context)