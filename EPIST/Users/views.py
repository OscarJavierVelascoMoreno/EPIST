from django.shortcuts import render

# Base views here.
def baseView(request):
    return render(request, "base_view.html")
