from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    context = {}
    return render(request, "shortener/index.html", context)


def result(request):
    try:
        url = request.POST["url"]
        alias = request.POST["alias"]
        context = {"url": url, "alias": alias}
        return render(request, "shortener/result.html", context)
    except KeyError:
        return HttpResponseRedirect(reverse("shortener:index"))
