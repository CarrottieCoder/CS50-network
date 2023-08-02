 
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    #API
    path("create", views.create, name="create"),
    path("api/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("api/<int:post_id>", views.get_post, name="get_post"),
]

