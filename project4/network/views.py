import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html',{
        'page_obj': page_obj, 
        'heading': 'All Posts'
        })

@login_required    
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('User does not exist')

    posts = Post.objects.all().filter(author=user)
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user in request.user.following.all():
        follows = "Unfollow"
    else:
        follows = "Follow"

    
    return render(request, 'network/profile.html',{
        'page_obj': page_obj, 
        "user": user,
        "follows": follows,
    })

@csrf_exempt
@login_required
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            post.save()
            return HttpResponse(status=205)
        else:
            return JsonResponse({"error": "You Have already liked this post"})
    else:
        return JsonResponse({"error": "Wrong request"}, status=404)

@csrf_exempt      
@login_required
def follow(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "PUT":
        if request.user not in user.followers.all():
            user.followers.add(request.user)
            user.save()
            print(user.followers)
            return HttpResponse(status=205)
            
        else:
            user.followers.remove(request.user)
            user.save()
            print(user.followers)
            return HttpResponse(status=205)

    elif request.method == 'GET':
        return JsonResponse(
            {"followers": user.followers.count()}, status=205
        )
    else:
        return JsonResponse({"error": "Wrong request"}, status=404)    
        

@login_required
def following(request):
    posts = Post.objects.filter(author__in=request.user.following.all()).order_by('-timestamp')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html',{
        'page_obj': page_obj, 
        'heading': 'Following'
        })

@csrf_exempt
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author:
        if request.method == "PUT":
            data = json.loads(request.body)
            if data.get("body") is not None:
                post.body = data["body"]
            post.save()
            return HttpResponse(status=204)
    else:
        return HttpResponse("Something went wrong")

@csrf_exempt
@login_required
def create(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    body = data.get("body", "")
    # Create a post
    post = Post(
        author=request.user,
        body=body,
    )
    post.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

def login_view(request):
    if request.method == "POST":

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
