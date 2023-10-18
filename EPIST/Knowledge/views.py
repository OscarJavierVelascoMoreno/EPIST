from django.shortcuts import render, redirect
from Projects.models import Project, User
from .models import Knowledge, KnowledgeType, KnowledgeStep
from .forms import KnowledgeForm, KnowledgeStepForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Knowledge views here.
@login_required()
def knowledges_list(request):
    knowledges = Knowledge.objects.all()
    order_knowledges = knowledges.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_knowledges, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "knowledges_list.html", {'page_obj': page_obj})

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
        return redirect("knowledges_list")
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
    form = KnowledgeStepForm(request.POST or None)
    knowledge = Knowledge.objects.get(id=id)
    if form.is_valid():
        knowledge_step = form.save(commit=False)
        knowledge_step.created_by = request.user
        knowledge_step.knowledge_id = knowledge
        knowledge_step.save()
        return redirect("knowledge_details", id=id)
    return render(request, "knowledge_step_create.html", {'form': form, 'knowledge': knowledge})

@login_required()
def knowledge_step_details(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    form = KnowledgeStepForm(request.POST or None, instance=knowledge_step)
    return render(request, "knowledge_step_details.html", {'form': form, 'knowledge_step': knowledge_step})

@login_required()
def knowledge_step_edit(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    form = KnowledgeStepForm(request.POST or None, instance=knowledge_step)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("knowledge_step_details", id=knowledge_step.id)
    return render(request, "knowledge_step_edit.html", {'form': form, 'knowledge_step': knowledge_step})

@login_required()
def knowledge_step_delete(request, id):
    knowledge_step = KnowledgeStep.objects.get(id=id)
    knowledge = knowledge_step.knowledge_id.id
    title = knowledge_step.title
    if request.method == 'POST':
        knowledge_step.delete()
        return redirect("knowledge_details", id=knowledge)
    return render(request, "knowledge_delete.html", {'title': title, 'knowledge': knowledge})
