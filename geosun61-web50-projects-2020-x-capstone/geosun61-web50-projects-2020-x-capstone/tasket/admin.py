from django.contrib import admin
from .models import User, Day, Task
# Register your models here.
admin.site.register(User)
admin.site.register(Day)
admin.site.register(Task)
