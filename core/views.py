from re import error
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import RegisterForm


def index(request):
    return render(request, "login.html")

def login_view(request):
    error_message = None
    context = {}
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        context = {"email": email, "password": password}
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or "links"
            return redirect(next_url)
        else:
            error_message = "Email or password is invalid"
        context = {
            "email": email,
            "password": password,
            "error": error_message,
        }
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("core:home")


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
    except IntegrityError as e:
        error_message = str(e)
        if (
            "auth_user_username_key" in error_message
            or "auth_user_email_key" in error_message
        ):
            context["error"] = "The email is already taken"
        else:
            context["error"] = "An error occured. Please check your input"
        return render(request, "register.html", context)
    except Exception as e:
        context["error"] = f"Error: {e}"
        return render(request, "register.html", context)

    return redirect("core:index")

def links_view(request):
    return render(request, "links.html", {'links': []})

def get_default_username(email):
    import re

    local_part = email.split("@")[0]
    return re.sub(r"[^a-zA-Z0-9]", "", local_part)


@login_required()
def home_view(request):
    return render(request, "index.html")
