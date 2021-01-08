from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here


class User(AbstractUser):
    pass


class Day(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="tasks")
    tasks = models.ManyToManyField("Task", related_name="tasks")

    date = models.DateField(auto_now_add=False, blank=True)
    datetime_created = models.DateTimeField(
        auto_now_add=True, auto_now=False, blank=True)

    completed_tasks = models.ManyToManyField(
        "Task", related_name="completedtask")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "tasks": [task.task_text for task in self.tasks.all()],
            "date": self.date.strftime("%b %#d %Y"),
            "datetime_created": self.datetime_created.strftime("%b %#d %Y, %#I:%M %p"),
            "completed_tasks": [comp_task.task_text for comp_task in self.completed_tasks.all()]
        }


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    task_text = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "task_text": self.task_text
        }
