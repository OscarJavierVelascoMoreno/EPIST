from django.shortcuts import render, redirect, HttpResponse
from .models import User
from .forms import UserForm

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
    return render(request, "users_list.html", {'users': order_users})

def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except Exception as e:
            return render(request, 'exception_popup.html', {'exception': e})
        return redirect('users_list')
    return render(request, "user_create.html", {'form': form})

def user_details(request):
    return render(request, "user_details.html")

def user_edit(request):
    return render(request, "user_edit.html")

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
