from django.urls import path

from . import views
from shortener import views as shortener_views

app_name = "core"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("links/", views.links_view, name="links"),
    path("links/create/", shortener_views.create_link_view, name="create_links_view"),
    path("links/edit/<int:id>", shortener_views.edit_link_view, name="create_links_view")
]
