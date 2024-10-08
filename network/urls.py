
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/", views.new_post, name="new_post"),
    path("profile/<int:user_id>/", views.profile_page, name="profile_page"),
    path("following/", views.following, name="following"),

    path("follow_unfollow/<int:user_id>", views.follow_unfollow, name="follow_unfollow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
