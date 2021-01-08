from django.urls import path

from . import views

urlpatterns = [
    path("", views.index,name="index"),
    path("wiki/<str:title>",views.wiki,name="wiki"),
    path("random", views.random1,name="random"),
    path("create",views.create,name="create"),
    path("edit/<str:title>",views.edit,name="edit"),
    path("search",views.search,name="search")
]
