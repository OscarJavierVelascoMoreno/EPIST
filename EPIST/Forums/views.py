from django.shortcuts import render, redirect
from Projects.models import Project, User
from .models import Forum, Discussion, Message
from .forms import ForumForm, DiscussionForm, MessageForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Forum views here.
@login_required()
def forums_list(request):
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
    return render(request, "forum_edit.html", {'form': form, 'forum': forum, 'projects': projects, 'discussions': discussions})

@login_required()
def forum_delete(request, id):
    forum = Forum.objects.get(id=id)
    title = forum.title
    if request.method == 'POST':
        forum.delete()
        return redirect("forums_list")
    return render(request, "forum_delete.html", {'title': title})

# Discussion views here.
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
    return render(request, "discussion_create.html", {'form': form, 'forum': forum, 'project': project})

@login_required()
def discussion_details(request, id):
    discussion = Discussion.objects.get(id=id)
    messages = Message.objects.filter(discussion_id=id)
    form = DiscussionForm(request.POST or None, instance=discussion)
    return render(request, "discussion_details.html", {'form': form, 'discussion': discussion, 'messages': messages})

@login_required()
def discussion_edit(request, id):
    discussion = Discussion.objects.get(id=id)
    messages = Message.objects.filter(discussion_id=id)
    form = DiscussionForm(request.POST or None, instance=discussion)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("discussion_details", id=discussion.id)
    return render(request, "discussion_edit.html", {'form': form, 'discussion': discussion, 'messages': messages})

@login_required()
def discussion_delete(request, id):
    discussion = Discussion.objects.get(id=id)
    forum = discussion.forum_id.id
    title = discussion.title
    if request.method == 'POST':
        discussion.delete()
        return redirect("forum_details", id=forum)
    return render(request, "discussion_delete.html", {'title': title, 'forum': forum})

# Message views here.
@login_required()
def message_create(request, id):
    form = MessageForm(request.POST or None)
    discussion = Discussion.objects.get(id=id)
    if form.is_valid():
        message = form.save(commit=False)
        message.created_by = request.user
        message.discussion_id = discussion
        message.save()
        return redirect("discussion_details", id=id)
    return render(request, "message_create.html", {'form': form, 'discussion': discussion})

@login_required()
def message_details(request, id):
    message = Message.objects.get(id=id)
    form = DiscussionForm(request.POST or None, instance=message)
    return render(request, "message_details.html", {'form': form, 'message': message})

@login_required()
def message_edit(request, id):
    message = Message.objects.get(id=id)
    form = MessageForm(request.POST or None, instance=message)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("message_details", id=message.id)
    return render(request, "message_edit.html", {'form': form, 'message': message})

@login_required()
def message_delete(request, id):
    message = Message.objects.get(id=id)
    discussion = message.discussion_id.id
    title = message.title
    if request.method == 'POST':
        message.delete()
        return redirect("discussion_details", id=discussion)
    return render(request, "message_delete.html", {'title': title, 'message': message})
