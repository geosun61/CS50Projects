import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Task, Day

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_page"))
    else:
        days = Day.objects.all().filter(user=request.user).order_by('date')
        return render(request, "tasket/index.html", {
            'days_obj': days
        })


def orderBy(request, orderbyQuery):
    days = Day.objects.all().filter(user=request.user).order_by(orderbyQuery)
    dayArr = []
    for day in days:
        dayArr.append(day.serialize())

    return JsonResponse({
        'days': dayArr
    }, status=200)


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasket/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "tasket/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tasket/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "tasket/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasket/register.html")


@login_required
def add_tasks_view(request):
    # load page
    if request.method == 'GET':
        return render(request, "tasket/addtask.html")

    # handle data
    if request.method == 'POST':
        data = json.loads(request.body)
        current_usr = request.user
        print(current_usr.id)

        # save date and tasks
        date = data.get('date', '')
        tasks = data.get('tasks', '')
        print(date)
        print(tasks)
        try:
            # if day returns exists
            day = Day.objects.get(user=current_usr,date=date)
            print(day)
            return JsonResponse({"error":'Date already exists'},status=400)
        except Day.DoesNotExist:
            try:
                taskArr = []
                for task_txt in tasks:
                    try:
                        # get task if task exists
                        task = Task.objects.get(task_text=task_txt)
                    except Task.DoesNotExist:
                        # create task if it does not exist
                        if task_txt == "" or task_txt is None:  # continue and do not save task if task entered is empty
                            continue
                        else:
                            x = task_txt.strip() #remove whitespace
                            task = Task(task_text=x)
                            task.save()
                            print(task)

                    taskArr.append(task)

                # create day
                day = Day(user=current_usr, date=date)
                day.save()

                # add tasks to day
                for task_obj in taskArr:
                    day1 = Day.objects.get(user=current_usr.id,date=date)
                    if task_obj.task_text is None or "":
                        continue
                    else:
                        day1.tasks.add(task_obj)

                day2 = Day.objects.get(user=current_usr, date=date)
                print('\n\n', day2)
                print('Day and Tasks have been saved\n\n')

                return JsonResponse({'message': 'Day and Tasks saved successfully',
                                     'day_obj': day2.serialize()}, status=201)
            except Exception as e:
                print('\nError: ', e, ' \n\nError: Saving Days and Tasks\n\n')
                return JsonResponse({'error': '\n\nError: Error saving day and tasks\n\n'}, status=400)



# complete task and mark off list
@login_required
def complete_task(request, day, task):
    if request.method == 'PUT':
        day_obj = Day.objects.get(id=day)
        task_obj = Task.objects.get(id=task)
        completed = is_completed(day_obj, task_obj)

        try:
            if completed:
                day_obj.completed_tasks.remove(task_obj)
            else:
                day_obj.completed_tasks.add(task_obj)

            comp = Day.objects.get(id=day)
            return JsonResponse({'message': 'Completed copying'}, status=201)
        except Exception as e:
            return JsonResponse({'error': e}, status=400)

@csrf_exempt
@login_required
def delete_day(request, day_id):
    if request.method == 'PUT':
        try:
            day = Day.objects.get(id=day_id)
            day.delete()
            return JsonResponse({"message": "Day " + str(day_id) + "deleted"})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Day " + str(day_id) + " not deleted" + e})

# API CALLS


@login_required
def get_day_obj(request, day_id):
    day_obj = Day.objects.get(id=day_id)
    return JsonResponse({'day': day_obj.serialize()})


@login_required
def get_task_obj(request, task_text):
    try:
        task_obj = Task.objects.get(task_text=task_text)
        return JsonResponse({'task': task_obj.serialize()})
    except Exception as e:
        raise


# check if task is completed
def is_completed(day, task):
    # function for checking if user task is completed
    completed = False
    for comp_task in day.completed_tasks.all():
        if comp_task.id == task.id:
            completed = True
    return completed
