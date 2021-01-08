import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    message = None
    if request.user.is_authenticated:
        posts = Post.objects.order_by('-timestamp')

        if 'edit_post' in request.session:
            if request.session['edit_post'] is True:
                message = "Edit was successful"
            del request.session['edit_post']

        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "message": message
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    current_user = User.objects.get(username=request.user.username)
    bd = data.get("body", "")
    likeN = 0

    if bd == [""]:
        return JsonResponse({"error": "Body needs to be filled"}, status=400)

    try:
        post = Post(poster=current_user,
                    body=bd,
                    likes=likeN)
        post.save()
        print(post)
    except Exception as e:
        return JsonResponse({"error": "Failed creating Post"}, status=400)

    return JsonResponse({"message": "Post created successfully."}, status=201)


@login_required
def user(request):
    posts = Post.objects.all().filter(poster=request.user).order_by('-timestamp')
    user = request.user
    paginator = Paginator(posts, 10)

    following_num = int(user.followed.count())
    posts_num = int(posts.count())

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "user_obj": user,
        "posts_num": posts_num,
        "following_num": following_num
    })

# TODO: fix user profiles


@login_required
def profile(request, user_id):
    user_page = User.objects.get(id=user_id)
    logged_in = request.user
    following = False

    posts = Post.objects.all().filter(poster=user_page.id).order_by('-timestamp')
    posts_num = posts.count()
    paginator = Paginator(posts, 10)

    following_num = int(user_page.followed.count())
    print(following_num)

    following = is_following(user_page, logged_in)
    print(following)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "user_obj": user_page,
        "following_num": following_num,
        "posts_num": posts_num,
        "following": following
    })


@login_required
def follow_posts(request):
    user = request.user
    following = user.followed.all()
    following_usernames = []

    for username in following:
        following_usernames.append(username.id)

    print(following_usernames)

    posts = Post.objects.all().filter(
        poster__in=following_usernames).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@login_required
@csrf_exempt
def follow_user(request, user_name):
    user = User.objects.get(username=user_name)
    logged_in = request.user
    following = is_following(user, logged_in)

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    try:
        if following:
            logged_in.followed.remove(user)
            return JsonResponse({"message": "Follow removed successfully.",
                                 "following": False}, status=201)
        else:
            logged_in.followed.add(user)
            return JsonResponse({"message": "Follow added successfully.",
                                 "following": True}, status=201)
    except Exception as e:
        return JsonResponse({"error": "(Follow button) Failed creating manytomany relationship"}, status=400)


@login_required
def get_user_data(request, user_name):
    try:
        user_data = User.objects.get(username=user_name)
        return JsonResponse({'user_data': user_data.serialize()}, status=200)
    except User.DoesNotExist as e:
        return JsonResponse({'error': f'User does not exist ${e}'}, status=400)


@login_required
def edit_post(request, post_id):
    post_obj = Post.objects.get(id=post_id)
    post_text = post_obj.body
    logged_in = request.user
    request.session['edit_post'] = False

    if logged_in != post_obj.poster:
        return JsonResponse({"error": "You cannot  edit this post"}, status=401)

    if request.method == 'GET':
        return render(request, "network/edit.html", {
            "post_text": post_text,
            "post_id": post_obj.id
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        editText = data.get("body")
        postid = data.get("id")

        try:
            post_obj.body = editText
            post_obj.save()
            post_edit = Post.objects.get(id=post_id)
            print(json.dumps(post_edit.serialize()))
            request.session['edit_post'] = True
            return JsonResponse({"message": json.dumps(post_edit.serialize())}, status=201)
        except Exception as e:
            request.session['edit_post'] = False
            return JsonResponse({"error": e}, status=400)


@csrf_exempt
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    logged_in = request.user
    liked = is_liked(post, logged_in)
    likes_count = post.liked_by.count()
    liked_value = False

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    try:
        if liked:
            post.liked_by.remove(logged_in)
            post.likes = likes_count
            post.save()
            liked_value = False

        else:
            post.liked_by.add(logged_in)
            post.likes = likes_count
            post.save()
            liked_value = True

        updated_postObj = Post.objects.get(id=post_id)
        return JsonResponse({"message": "Follow added successfully.",
                             "liked": liked_value,
                             "likes": updated_postObj.likes}, status=201)
    except Exception as e:
        return JsonResponse({"error": "(Like button) Failed creating manytomany relationship"}, status=400)


def is_following(user, logged_in):
    # function for checking if current logged in user is following a user
    following = False
    for followed in logged_in.followed.all():
        if followed == user:
            following = True
    return following


def is_liked(post, logged_in):
    # function for checking if current logged in user liked a post
    liked = False
    for liked_by in post.liked_by.all():
        if liked_by == logged_in:
            liked = True
    return liked
