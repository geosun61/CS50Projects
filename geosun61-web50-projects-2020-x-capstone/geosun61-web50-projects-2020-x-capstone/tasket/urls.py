from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("orderby/<str:orderbyQuery>",views.orderBy,name="orderby"),
    path("completetask/<int:day>/<int:task>",views.complete_task, name="completedtask"),
    path("add", views.add_tasks_view,name="addtasks"),
    path("delete/<int:day_id>",views.delete_day,name="deleteday"),

    #login and register links
    path("login", views.login_view, name="login_page"),
    path("logout", views.logout_view, name="logout_user"),
    path("register", views.register_view, name="register_page"),

    #API links
    path("day/<int:day_id>",views.get_day_obj,name="getday"),
    path("task/<str:task_text>",views.get_task_obj,name="gettask")

]
