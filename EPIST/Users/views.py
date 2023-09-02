from django.shortcuts import render, redirect
from Projects.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            selected_user = form.save()
            selected_user.password = make_password(selected_user.password)
            selected_user.save()
        except Exception as e:
            return render(request, 'exception_popup.html', {'exception': e})
        return redirect("user_details", id=selected_user.id)
    return render(request, "user_create.html", {'form': form})

def user_details(request, id):
    selected_user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=selected_user)
    return render(request, "user_details.html", {'form': form, 'selected_user': selected_user})

def user_edit(request, id):
    selected_user = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=selected_user)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect("user_details", id=selected_user.id)
    return render(request, "user_edit.html", {'form': form, 'selected_user': selected_user})

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
    selected_user = User.objects.get(id=id)
    old_error = False
    new_error = False
    if request.method == 'POST':
        old_password = request.POST['old_password']
        if selected_user.check_password(old_password):
            new_password = request.POST['new_password']
            new_password_confirm = request.POST['new_password_confirm']
            if new_password_confirm == new_password:
                selected_user.password = make_password(new_password)
                selected_user.save()
                return redirect("user_details", id=selected_user.id)
            else:
                new_error = "La nueva contraseña y su confirmación no coinciden."
                return render(request, "user_change_password.html", {'selected_user':selected_user, "new_error": new_error, "old_error": old_error})
        else:
            old_error = "La contraseña no coincide con la antigua contraseña."
            return render(request, "user_change_password.html", {'selected_user':selected_user, "new_error": new_error, "old_error": old_error})
    return render(request, "user_change_password.html", {'selected_user':selected_user, "new_error": new_error, "old_error": old_error})

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

def page_logout(request):
    logout(request)
    return redirect('login')
