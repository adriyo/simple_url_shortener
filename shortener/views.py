from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UrlMapping
from django.utils import timezone
from django.db import IntegrityError


def index(request):
    context = {}
    return render(request, "shortener/index.html", context)


def result(request):
    try:
        url = request.POST["url"]
        alias = request.POST["alias"]
        context = {"url": url, "alias": alias}
    except KeyError:
        return redirect(reverse("shortener:index"))

    try:
        is_url_invalid = len(url) < 5
        if is_url_invalid:
            context = {
                "url": url,
                "alias": alias,
                "error_url": "URL is invalid",
            }
            return render(request, "shortener/index.html", context)

        user = request.user
        if user.is_anonymous:
            user = None

        url_mapping = UrlMapping(
            short_url=alias,
            long_url=url,
            created_at=timezone.now(),
            expired_at=timezone.now() + timezone.timedelta(days=30),
            user=user,
            click_count=0,
        )
        url_mapping.save()
        context["message"] = " successfully created"
        current_host = request.build_absolute_uri("/")
        context["generated_url"] = f"{current_host}s/{alias}"
        if user is not None:
            return redirect("core:links")
        return render(request, "shortener/index.html", context)

    except IntegrityError:
        context.update({"error": "URL or Alias already exists"})
        return render(request, "shortener/index.html", context)


def redirect_url(request, alias):
    try:
        url_mapping = UrlMapping.objects.get(short_url=alias)
        url_mapping.click_count += 1
        url_mapping.save()
        return HttpResponseRedirect(url_mapping.long_url)
    except UrlMapping.DoesNotExist:
        context = {"error_message": "URL Not Found"}
        return render(request, "shortener/error.html", context)

def create_link_view(request):
    return render(request, "shortener/create.html")

def edit_link_view(request, id):
    link = UrlMapping.objects.get(id=id)
    return render(request, "shortener/create.html", {'link': link})
