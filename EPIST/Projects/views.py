from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# projects views here.
@login_required()
def projects_list(request):
    projects = Project.objects.all()
    order_projects = projects.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_projects, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "projects_list.html", {'page_obj': page_obj})

@login_required()
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        return redirect("project_details", id=project.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'exception': form.errors,}
        cleaned_data = form.cleaned_data
        basic_data.update(cleaned_data)
        return render(request, "project_create.html", basic_data)
    return render(request, "project_create.html", {'form': form})

@login_required()
def project_details(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(request.POST or None, instance=project)
    return render(request, "project_details.html", {'form': form, 'project': project})

@login_required()
def project_edit(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("project_details", id=project.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'exception': form.errors,}
        cleaned_data = form.cleaned_data
        basic_data.update(cleaned_data)
        return render(request, "project_create.html", basic_data)
    return render(request, "project_edit.html", {'form': form, 'project': project})

@login_required()
def project_delete(request, id):
    project = Project.objects.get(id=id)
    title = project.title
    if request.method == 'POST':
        project.delete()
        return redirect("projects_list")
    return render(request, "project_delete.html", {'title': title, 'id': id})

