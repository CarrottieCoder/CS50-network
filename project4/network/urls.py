 
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
    path("<int:post_id>", views.edit_post, name="get_post"),
    path("<int:post_id>/edit", views.edit_post, name="edit_post"),
]

