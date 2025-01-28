from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return render(request, "index.html")

def login(request):
    try:
        email = request.POST["email"]
        password = request.POST["password"]
        context = {"email": email, "password": password}
    except KeyError:
        return redirect(reverse("core:index"))
    context = {
        "email": email,
        "password": password,
        "error": "Email or password is invalid",
    }
    return render(request, "index.html", context)
