from django.shortcuts import render, redirect
from Projects.models import Project, User
from .models import Knowledge, KnowledgeType, KnowledgeStep
from .forms import KnowledgeForm, KnowledgeStepForm, KnowledgeTypeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Knowledge views here.
@login_required()
def knowledge_list(request):
    knowledge = Knowledge.objects.all()
    order_knowledge = knowledge.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_knowledge, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "knowledge_list.html", {'page_obj': page_obj})

@login_required()
def knowledge_create(request):
    projects = Project.objects.all()
    types = KnowledgeType.objects.all()
    form = KnowledgeForm(request.POST or None)
    if form.is_valid():
        knowledge = form.save(commit=False)
        knowledge.created_by = request.user
        knowledge.save()
        return redirect("knowledge_details", id=knowledge.id)
    elif form.errors:
        project_selected = request.POST.get('project_id')
        type_selected = request.POST.get('type_id')
        basic_data = {
            'form': form,
            'projects': projects,
            'types': types,
            'project_selected': project_selected,
            'type_selected': type_selected,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "knowledge_create.html", basic_data)
    return render(request, "knowledge_create.html", {'form': form, 'projects': projects, 'types': types})

@login_required()
def knowledge_details(request, id):
    knowledge = Knowledge.objects.get(id=id)
    form = KnowledgeForm(request.POST or None, instance=knowledge)
    steps = KnowledgeStep.objects.filter(knowledge_id=id)
    return render(request, "knowledge_details.html", {'form': form, 'knowledge': knowledge, 'steps': steps})

@login_required()
def knowledge_edit(request, id):
    projects = Project.objects.all()
    types = KnowledgeType.objects.all()
    steps = KnowledgeStep.objects.filter(knowledge_id=id)
    knowledge = Knowledge.objects.get(id=id)
    form = KnowledgeForm(request.POST or None, instance=knowledge)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("knowledge_details", id=knowledge.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'knowledge': knowledge,
            'projects': projects,
            'types': types,
            'steps': steps,
            'exception': form.errors}
        return render(request, "knowledge_edit.html", basic_data)
    return render(request, "knowledge_edit.html", {'form': form, 'knowledge': knowledge, 'projects': projects, 'types': types, 'steps': steps})

@login_required()
def knowledge_delete(request, id):
    knowledge = Knowledge.objects.get(id=id)
    title = knowledge.title
    if request.method == 'POST':
        knowledge.delete()
        return redirect("knowledge_list")
    return render(request, "knowledge_delete.html", {'title': title, 'id': id})

@login_required()
def knowledge_to_approval(request, id):
    knowledge = Knowledge.objects.get(id=id)
    knowledge.state = 'for_approval'
    knowledge.save()
    return redirect("knowledge_details", id=id)

@login_required()
def knowledge_approve(request, id):
    knowledge = Knowledge.objects.get(id=id)
    knowledge.state = 'approved'
    knowledge.save()
    return redirect("knowledge_details", id=id)

# Knowledge Step views here.
@login_required()
def knowledge_step_create(request, id):
    form = KnowledgeStepForm(request.POST or None, files=request.FILES)
    knowledge = Knowledge.objects.get(id=id)
    if form.is_valid():
        knowledge_step = form.save()
        knowledge_step.created_by = request.user
        knowledge_step.save()
        return redirect("knowledge_step_details", id=knowledge_step.id)
    return render(request, "knowledge_step_create.html", {'form': form, 'knowledge': knowledge})

@login_required()
def knowledge_step_details(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    form = KnowledgeStepForm(request.POST or None, instance=knowledge_step)
    return render(request, "knowledge_step_details.html", {'form': form, 'knowledge_step': knowledge_step})

@login_required()
def knowledge_step_edit(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    form = KnowledgeStepForm(request.POST or None, instance=knowledge_step, files=request.FILES)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("knowledge_step_details", id=knowledge_step.id)
    elif form.errors and request.method == 'POST':
        basic_data = {
            'form': form,
            'knowledge_step': knowledge_step,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "knowledge_step_edit.html", basic_data)
    return render(request, "knowledge_step_edit.html", {'form': form, 'knowledge_step': knowledge_step})

@login_required()
def knowledge_step_delete(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    knowledge = knowledge_step.knowledge_id.id
    title = knowledge_step.title
    if request.method == 'POST':
        knowledge_step.delete()
        return redirect("knowledge_details", id=knowledge)
    return render(request, "knowledge_delete.html", {'title': title, 'knowledge': knowledge, 'id': id})

# Knowledge Type views here.
@login_required()
def knowledge_types_list(request):
    knowledge_type = KnowledgeType.objects.all()
    order_knowledge_type = knowledge_type.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_knowledge_type, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "knowledge_types_list.html", {'page_obj': page_obj})

@login_required()
def knowledge_type_create(request):
    form = KnowledgeTypeForm(request.POST or None)
    if form.is_valid():
        knowledge_type = form.save(commit=False)
        knowledge_type.save()
        return redirect("knowledge_type_details", id=knowledge_type.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "knowledge_type_create.html", basic_data)
    return render(request, "knowledge_type_create.html", {'form': form})

@login_required()
def knowledge_type_details(request, id):
    knowledge_type = KnowledgeType.objects.get(id=id)
    form = KnowledgeTypeForm(request.POST or None, instance=knowledge_type)
    return render(request, "knowledge_type_details.html", {'form': form, 'knowledge_type': knowledge_type})

@login_required()
def knowledge_type_edit(request, id):
    knowledge_type = KnowledgeType.objects.get(id=id)
    form = KnowledgeTypeForm(request.POST or None, instance=knowledge_type)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("knowledge_type_details", id=knowledge_type.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'knowledge_type': knowledge_type,
            'exception': form.errors}
        return render(request, "knowledge_type_edit.html", basic_data)
    return render(request, "knowledge_type_edit.html", {'form': form, 'knowledge_type': knowledge_type})

@login_required()
def knowledge_type_delete(request, id):
    knowledge_type = KnowledgeType.objects.get(id=id)
    title = knowledge_type.title
    if request.method == 'POST':
        knowledge_type.delete()
        return redirect("knowledge_types_list")
    return render(request, "knowledge_type_delete.html", {'title': title, 'id': id})
