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
        is_alias_invalid = len(alias) < 5
        if is_url_invalid or is_alias_invalid:
            context = {
                "url": url,
                "alias": alias,
                "error_url": "URL is invalid",
                "error_alias": "Path is invalid",
            }
            return render(request, "shortener/index.html", context)

        url_mapping = UrlMapping(
            short_url=alias,
            long_url=url,
            created_at=timezone.now(),
            expired_at=timezone.now() + timezone.timedelta(days=30),
            user=None,
            click_count=0,
        )
        url_mapping.save()
        context["message"] = " successfully created"
        current_host = request.build_absolute_uri("/")
        context["generated_url"] = f"{current_host}{alias}"
        return render(request, "shortener/index.html", context)
    except IntegrityError:
        context.update({"error": "URL or Alias already exists"})
        return render(request, "shortener/index.html", context)
