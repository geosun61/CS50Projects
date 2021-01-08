
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #new paths
    path("post",views.post,name="createpost"),
    path("post/edit/<int:post_id>",views.edit_post,name="editpost"),
    path("post/like/<int:post_id>",views.like_post,name="likepost"),
    path("profile",views.user,name="user"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("following",views.follow_posts,name="following_posts"),
    path("follow/<str:user_name>",views.follow_user,name="follow_u"),
    path("user/<str:user_name>",views.get_user_data,name="get_user_data")

]
