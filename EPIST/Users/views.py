from django.shortcuts import render, redirect
from Projects.models import User, Project
from django.contrib.auth import authenticate, login, logout
from EPIST.passwordValidators import ComplexPasswordValidator
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from .forms import UserForm, GroupForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


# Welcome view here.
@login_required()
def welcome(request):
    return render(request, "welcome.html")

@login_required()
def settings(request):
    return render(request, "settings.html")

# Users views here.
@login_required()
def users_list(request):

    name = request.GET.get('search')
    if name:
        users = User.objects.filter(first_name__icontains=name)
    else:
        users = User.objects.all()

    order_users = users.order_by('first_name')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_users, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "users_list.html", {'page_obj': page_obj})

@login_required()
def user_create(request):
    form = UserForm(request.POST or None)
    projects_list = Project.objects.all()
    groups_list = Group.objects.all()
    if form.is_valid():
        try:
            selected_user = form.save()
            validator = ComplexPasswordValidator()
            validator.validate(password=selected_user.password)
            selected_user.password = make_password(selected_user.password)
            for project in request.POST.getlist('projects'):
                selected_user.project_ids.add(Project.objects.get(id=int(project)))
            for group in request.POST.getlist('groups'):
                selected_user.groups.add(Group.objects.get(id=int(group)))
            selected_user.save()
        except Exception as e:
            projects_selected = request.POST.getlist('projects')
            groups_selected = request.POST.getlist('groups')
            basic_data = {
                'form': form,
                'projects_list': projects_list,
                'projects_selected': projects_selected,
                'groups_list': groups_list,
                'groups_selected': groups_selected,
                'exception': e}
            cleaned_data = form.cleaned_data
            basic_data.update(cleaned_data)
            selected_user.delete()
            return render(request, 'user_create.html', basic_data)
        return redirect("user_details", id=selected_user.id)
    elif form.errors:
        projects_selected = request.POST.getlist('projects')
        groups_selected = request.POST.getlist('groups')
        basic_data = {
            'form': form,
            'projects_list': projects_list,
            'projects_selected': projects_selected,
            'groups_list': groups_list,
            'groups_selected': groups_selected,
            'exception': form.errors}
        cleaned_data = form.cleaned_data
        basic_data.update(cleaned_data)
        return render(request, 'user_create.html', basic_data)
    return render(request, "user_create.html", {'form': form, 'projects_list': projects_list, 'groups_list': groups_list})

@login_required()
def user_details(request, id):
    selected_user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=selected_user)
    return render(request, "user_details.html", {'form': form, 'selected_user': selected_user})

@login_required()
def user_edit(request, id):
    selected_user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=selected_user)
    projects_list = Project.objects.all()
    groups_list = Group.objects.all()
    projects_selected = selected_user.project_ids.all()
    groups_selected = selected_user.groups.all()
    if form.is_valid() and request.method == 'POST':
        model_edit_validation(
            request,
            selected_user.project_ids,
            'projects',
            Project,
            projects_selected)
        model_edit_validation(
            request,
            selected_user.groups,
            'groups',
            Group,
            groups_selected)
        selected_user.save()
        form.save()
        return redirect("user_details", id=selected_user.id)
    elif form.errors:
        projects_selected = selected_user.project_ids.all()
        groups_selected = selected_user.groups.all()
        basic_data = {
            'form': form,
            'projects_list': projects_list,
            'projects_selected': projects_selected,
            'groups_list': groups_list,
            'groups_selected': groups_selected,
            'exception': form.errors}
        cleaned_data = form.cleaned_data
        basic_data.update(cleaned_data)
        return render(request, 'user_edit.html', basic_data)
    return render(request, "user_edit.html", {
        'form': form,
        'selected_user': selected_user,
        'projects_list': projects_list,
        'projects_selected': projects_selected,
        'groups_list': groups_list,
        'groups_selected': groups_selected})

def model_edit_validation(request, user_field, field_name, model, records_selected):
    record_ids = [int(x) for x in request.POST.getlist(field_name)]
    if record_ids:
        new_records_selected = model.objects.filter(id__in=record_ids)
        if list(new_records_selected) != list(record_ids):
            for old_project in records_selected:
                user_field.remove(old_project)
            for project in new_records_selected:
                user_field.add(project)
    else:
        for old_project in records_selected:
            user_field.remove(old_project)

@login_required()
def user_delete(request, id):
    user = User.objects.get(id=id)
    first_name = user.first_name
    last_name = user.last_name
    if request.method == 'POST':
        user.delete()
        return redirect("users_list")
    return render(request, "user_delete.html", {
        'id': id,
        'first_name': first_name,
        'last_name': last_name
        })

@login_required()
def user_change_password(request, id):
    selected_user = User.objects.get(id=id)
    old_error = False
    new_error = False
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_confirm = request.POST['new_password_confirm']
        if selected_user.check_password(old_password):
            if new_password_confirm == new_password:
                selected_user.password = make_password(new_password)
                try:
                    validator = ComplexPasswordValidator()
                    validator.validate(password=new_password)
                except Exception as e:
                    basic_data = {
                        'selected_user': selected_user,
                        "new_error": e,
                        "old_error": old_error,
                        "old_password": request.POST['old_password'],
                        "new_password": new_password,
                        "new_password_confirm": new_password_confirm}
                    return render(request, "user_change_password.html", basic_data)
                selected_user.save()
                return redirect("user_details", id=selected_user.id)
            else:
                new_error = "La nueva contraseña y su confirmación no coinciden."
                basic_data = {
                        'selected_user': selected_user,
                        "new_error": new_error,
                        "old_error": old_error,
                        "old_password": request.POST['old_password'],
                        "new_password": new_password,
                        "new_password_confirm": new_password_confirm}
                return render(request, "user_change_password.html", basic_data)
        else:
            old_error = "La contraseña no coincide con la antigua contraseña."
            basic_data = {
                        'selected_user': selected_user,
                        "new_error": new_error,
                        "old_error": old_error,
                        "old_password": request.POST['old_password'],
                        "new_password": new_password,
                        "new_password_confirm": new_password_confirm}
            return render(request, "user_change_password.html", basic_data)
    return render(request, "user_change_password.html", {'selected_user':selected_user, "new_error": new_error, "old_error": old_error})

# Login views here
def page_login(request):
    msg_error = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            msg_error = "Credenciales incorrectas, por favor intente nuevamente."
            return render(request, "login.html", {'msg_error': msg_error})

    return render(request, "login.html")

@login_required()
def page_logout(request):
    logout(request)
    return redirect('login')

# Group views here
@login_required()
def groups_list(request):

    name = request.GET.get('search')
    if name:
        groups = Group.objects.filter(name__icontains=name)
    else:
        groups = Group.objects.all()

    order_groups = groups.order_by('name')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(order_groups, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "groups_list.html", {'page_obj': page_obj})

@login_required()
def group_create(request):
    form = GroupForm(request.POST or None)
    permissions_list = Permission.objects.all()
    if form.is_valid():
        new_group = form.save()
        for permission in request.POST.getlist('permissions'):
            new_group.permissions.add(Permission.objects.get(id=int(permission)))
        new_group.save()
        return redirect("group_details", id=new_group.id)
    elif form.errors:
        permissions_selected = request.POST.getlist('permissions')
        basic_data = {
            'form': form,
            'permissions_list': permissions_list,
            'permissions_selected': permissions_selected,
            'exception': form.errors}
        cleaned_data = form.cleaned_data
        basic_data.update(cleaned_data)
        return render(request, 'group_create.html', basic_data)
    return render(request, "group_create.html", {'form': form, 'permissions_list': permissions_list})

@login_required()
def group_details(request, id):
    selected_group = Group.objects.get(id=id)
    form = GroupForm(request.POST or None, instance=selected_group)
    return render(request, "group_details.html", {'form': form, 'selected_group': selected_group})

@login_required()
def group_edit(request, id):
    selected_group = Group.objects.get(id=id)
    form = GroupForm(request.POST or None, instance=selected_group)
    permissions_selected = selected_group.permissions.all()
    permissions_list = Permission.objects.all()
    if form.is_valid() and request.method == 'POST':
        permissions_ids = [int(x) for x in request.POST.getlist('permissions')]
        if permissions_ids:
            new_permissions_selected = Permission.objects.filter(id__in=permissions_ids)
            if list(new_permissions_selected) != list(permissions_selected):
                for old_permission in permissions_selected:
                    selected_group.permissions.remove(old_permission)
                for permission in new_permissions_selected:
                    selected_group.permissions.add(permission)
        else:
            for old_permission in permissions_selected:
                selected_group.permissions.remove(old_permission)
        selected_group.save()
        form.save()
        return redirect("group_details", id=selected_group.id)
    return render(request, "group_edit.html", {'form': form, 'selected_group': selected_group, 'permissions_list': permissions_list, 'permissions_selected': permissions_selected})

@login_required()
def group_delete(request, id):
    group = Group.objects.get(id=id)
    group_name = group.name
    if request.method == 'POST':
        group.delete()
        return redirect("groups_list")
    return render(request, "group_delete.html", {
        'group_name': group_name,
        'id': id})
