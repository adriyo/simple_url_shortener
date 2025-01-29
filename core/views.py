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


def register(request):
    if request.method == "POST":
        return submitRegistration(request)

    return render(request, "register.html")


def submitRegistration(request):
    try:
        email = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        context = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "username": get_default_username(email),
        }
    except KeyError:
        return redirect(reverse("core:register"))
    print(context)
    return redirect("core:index")


def get_default_username(email):
    import re

    local_part = email.split("@")[0]
    return re.sub(r"[^a-zA-Z0-9]", "", local_part)
