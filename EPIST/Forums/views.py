from django.shortcuts import render, redirect
from Projects.models import Project, User
from .models import Forum, Discussion, Message
from .forms import ForumForm, DiscussionForm, MessageForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from Knowledge.forms import KnowledgeForm
from Knowledge.models import KnowledgeStep

# Forum views here.
@login_required()
def forums_list(request):
    title = request.GET.get('search')
    if title:
        forums = Forum.objects.filter(title__icontains=title)
    else:
        forums = Forum.objects.all()

    order_forums = forums.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_forums, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "forums_list.html", {'page_obj': page_obj})

@login_required()
def forum_create(request):
    projects = Project.objects.all()
    form = ForumForm(request.POST or None)
    if form.is_valid():
        forum = form.save(commit=False)
        forum.created_by = request.user
        forum.save()
        return redirect("forum_details", id=forum.id)
    elif form.errors:
        project_selected = request.POST.get('project_id')
        basic_data = {
            'form': form,
            'projects': projects,
            'project_selected': project_selected,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "forum_create.html", basic_data)
    return render(request, "forum_create.html", {'form': form, 'projects': projects})

@login_required()
def forum_details(request, id):
    forum = Forum.objects.get(id=id)
    form = ForumForm(request.POST or None, instance=forum)
    discussions = Discussion.objects.filter(forum_id=id)
    return render(request, "forum_details.html", {'form': form, 'forum': forum, 'discussions': discussions})

@login_required()
def forum_edit(request, id):
    projects = Project.objects.all()
    discussions = Discussion.objects.filter(forum_id=id)
    forum = Forum.objects.get(id=id)
    form = ForumForm(request.POST or None, instance=forum)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("forum_details", id=forum.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'forum': forum,
            'projects': projects,
            'discussions': discussions,
            'exception': form.errors}
        return render(request, "forum_edit.html", basic_data)
    return render(request, "forum_edit.html", {'form': form, 'forum': forum, 'projects': projects, 'discussions': discussions})

@login_required()
def forum_delete(request, id):
    forum = Forum.objects.get(id=id)
    title = forum.title
    if request.method == 'POST':
        forum.delete()
        return redirect("forums_list")
    return render(request, "forum_delete.html", {'title': title, 'id': id})

# Discussion views here.
@login_required()
def discussions_list(request):
    title = request.GET.get('search')
    if title:
        discussions = Discussion.objects.filter(title__icontains=title)
    else:
        discussions = Discussion.objects.all()

    order_discussions = discussions.order_by('title')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_discussions, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "discussions_list.html", {'page_obj': page_obj})

@login_required()
def discussion_create(request, id):
    form = DiscussionForm(request.POST or None)
    forum = Forum.objects.get(id=id)
    project = Project.objects.get(id=forum.project_id.id)
    if form.is_valid():
        discussion = form.save(commit=False)
        discussion.created_by = request.user
        discussion.forum_id = forum
        discussion.project_id = project
        discussion.save()
        return redirect("discussion_details", id=discussion.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'forum': forum,
            'project': project,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "discussion_create.html", basic_data)
    return render(request, "discussion_create.html", {'form': form, 'forum': forum, 'project': project})

@login_required()
def discussion_details(request, id):
    discussion = Discussion.objects.get(id=id)
    messages = Message.objects.filter(discussion_id=id)
    form = DiscussionForm(request.POST or None, instance=discussion)
    return render(request, "discussion_details.html", {'form': form, 'discussion': discussion, 'messages': messages})

@login_required()
def discussions_details_list(request, id):
    discussion = Discussion.objects.get(id=id)
    messages = Message.objects.filter(discussion_id=id)
    form = DiscussionForm(request.POST or None, instance=discussion)
    return render(request, "discussions_details_list.html", {'form': form, 'discussion': discussion, 'messages': messages})

@login_required()
def discussion_edit(request, id):
    discussion = Discussion.objects.get(id=id)
    messages = Message.objects.filter(discussion_id=id)
    form = DiscussionForm(request.POST or None, instance=discussion)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("discussion_details", id=discussion.id)
    elif form.errors:
        basic_data = {
            'form': form,
            'messages': messages,
            'discussion': discussion,
            'exception': form.errors}
        return render(request, "discussion_edit.html", basic_data)
    return render(request, "discussion_edit.html", {'form': form, 'discussion': discussion, 'messages': messages})

@login_required()
def create_knowledge(request, id):
    discussion = Discussion.objects.get(id=id)
    knowledge = False
    try:
        knowledge = discussion.create_knowledge()
        form = KnowledgeForm(request.POST or None, instance=knowledge)
        steps = KnowledgeStep.objects.filter(knowledge_id=knowledge.id)
    except Exception as e:
        if knowledge:
            knowledge.delete()
        return render(request, "discussion_details.html", {'discussion': discussion, 'exception': e})
    return render(request, "knowledge_details.html", {'form': form, 'knowledge': knowledge, 'steps': steps})

@login_required()
def discussion_delete(request, id):
    discussion = Discussion.objects.get(id=id)
    forum = discussion.forum_id.id
    title = discussion.title
    if request.method == 'POST':
        discussion.delete()
        return redirect("forum_details", id=forum)
    return render(request, "discussion_delete.html", {'title': title, 'forum': forum, 'id': id})

# Message views here.
@login_required()
def message_create(request, id):
    form = MessageForm(request.POST or None, files=request.FILES)
    discussion = Discussion.objects.get(id=id)
    if form.is_valid() and request.method == 'POST':
        message = form.save()
        message.created_by = request.user
        message.save()
        return redirect("message_details", id=message.id)
    elif form.errors and request.method == 'POST':
        basic_data = {
            'form': form,
            'discussion': discussion,
            'exception': form.errors}
        basic_data.update(form.cleaned_data)
        return render(request, "message_create.html", basic_data)
    return render(request, "message_create.html", {'form': form, 'discussion': discussion})

@login_required()
def message_details(request, id):
    message = Message.objects.get(id=id)
    form = DiscussionForm(request.POST or None, instance=message)
    return render(request, "message_details.html", {'form': form, 'message': message})

@login_required()
def relevant_message(request, id):
    message = Message.objects.get(id=id)
    message.mark_relevant = True
    message.save()
    form = DiscussionForm(request.POST or None, instance=message)
    return render(request, "message_details.html", {'form': form, 'message': message})

@login_required()
def message_edit(request, id):
    message = Message.objects.get(id=id)
    form = MessageForm(request.POST or None, instance=message, files=request.FILES)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("message_details", id=message.id)
    elif form.errors and request.method == 'POST':
        basic_data = {
            'form': form,
            'message': message,
            'exception': form.errors}
        return render(request, "message_edit.html", basic_data)
    return render(request, "message_edit.html", {'form': form, 'message': message})

@login_required()
def message_delete(request, id):
    message = Message.objects.get(id=id)
    discussion = message.discussion_id.id
    title = message.title
    if request.method == 'POST':
        message.delete()
        return redirect("discussion_details", id=discussion)
    return render(request, "message_delete.html", {'title': title, 'message': message, 'id': id})
