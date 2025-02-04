from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm


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
    form = RegisterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        context = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "username": get_default_username(email),
        }
    else:
        error_list = [msg for sublist in form.errors.values() for msg in sublist]
        error_text = "\n".join(error_list)
        error_message = f"Error: {error_text}"
        return render(request, "register.html", {"error": error_message})

    try:
        user = User.objects.create_user(
            context["username"],
            email=context["email"],
            password=context["password"],
            first_name=context["first_name"],
            last_name=context["last_name"],
        )
        user.save()
    except Exception as e:
        context["error"] = f"Error: {e}"
        return render(request, "register.html", context)

    return redirect("core:index")


def get_default_username(email):
    import re

    local_part = email.split("@")[0]
    return re.sub(r"[^a-zA-Z0-9]", "", local_part)
