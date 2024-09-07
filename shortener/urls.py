from django.urls import path

from . import views

app_name = "shortener"
urlpatterns = [
    path("", views.index, name="index"),
    path("generate_alias/", views.result, name="generate_alias"),
]
