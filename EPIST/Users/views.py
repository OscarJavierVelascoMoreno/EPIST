from django.shortcuts import render, redirect, HttpResponse
from Projects.models import User
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Base views here.
def baseView(request):
    return render(request, "base_view.html")

# Welcome view here.
def welcome(request):
    return render(request, "welcome.html")

# Users views here.

def users_list(request):
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

def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        try:
            user = form.save()
            user.password = make_password(user.password)
            user.save()
        except Exception as e:
            return render(request, 'exception_popup.html', {'exception': e})
        return redirect("user_details", id=user.id)
    return render(request, "user_create.html", {'form': form})

def user_details(request, id):
    user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=user)
    return render(request, "user_details.html", {'form': form, 'user': user})

def user_edit(request, id):
    user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("user_details", id=user.id)
    return render(request, "user_edit.html", {'form': form, 'user': user})

def user_delete(request, id):
    user = User.objects.get(id=id)
    first_name = user.first_name
    last_name = user.last_name
    if request.method == 'POST':
        user.delete()
        return redirect("users_list")
    return render(request, "user_delete.html", {
        'first_name': first_name,
        'last_name': last_name
        })

def user_change_password(request, id):
    user = User.objects.get(id=id)
    old_error = False
    new_error = False
    if request.method == 'POST':
        old_password = request.POST['old_password']
        if user.check_password(old_password):
            new_password = request.POST['new_password']
            new_password_confirm = request.POST['new_password_confirm']
            if new_password_confirm == new_password:
                user.password = make_password(new_password)
                user.save()
                return redirect("user_details", id=user.id)
            else:
                new_error = "La nueva contraseña y su confirmación no coinciden."
                return render(request, "user_change_password.html", {'user':user, "new_error": new_error, "old_error": old_error})
        else:
            old_error = "La contraseña no coincide con la antigua contraseña."
            return render(request, "user_change_password.html", {'user':user, "new_error": new_error, "old_error": old_error})
    return render(request, "user_change_password.html", {'user':user, "new_error": new_error, "old_error": old_error})
