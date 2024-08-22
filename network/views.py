import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser

from .models import User, Like, Post, Following


def index(request):
    posts = Post.objects.all().order_by('-id')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    if isinstance(request.user, AnonymousUser):
        liked_post_ids = set()
    else:
        liked_posts = Like.objects.filter(user=request.user, like=True).values_list('post_id', flat=True)
        liked_post_ids = set(liked_posts)

    return render(request, "network/index.html", {
        "posts":page_obj,
        "page_obj":page_obj,
        "liked_post_ids":liked_post_ids
    })


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

def new_post(request):
    if request.method == "POST":
        post = Post(user=request.user, text=request.POST["text"], likes=0)
        post.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, 'network/newpost.html')

def profile_page(request, user_id):
    
    profile_user = User.objects.get(pk=user_id)
    current_user = request.user
    posts = Post.objects.filter(user=profile_user).order_by('-id')
    followers = Following.objects.filter(following = profile_user).count()
    followings = Following.objects.filter(user = profile_user).count()

    is_following = Following.objects.filter(user=current_user, following=profile_user).exists()

    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    if isinstance(request.user, AnonymousUser):
        liked_post_ids = set()
    else:
        liked_posts = Like.objects.filter(user=request.user, like=True).values_list('post_id', flat=True)
        liked_post_ids = set(liked_posts)

    return render(request, 'network/profile.html', {
        "profile":profile_user,
        "posts":page_obj,
        "page_obj":page_obj,
        "is_following":is_following,
        "followers" : followers,
        "followings": followings,
        "liked_post_ids":liked_post_ids

    })

def following(request):
    current_user = request.user
    followings = Following.objects.filter(user = current_user)
    postings = []
    for follow in followings:
        user = follow.following
        posts = Post.objects.filter(user = user).order_by('-id')
        postings.extend(posts)

    p = Paginator(postings, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/index.html", {
        "posts":page_obj,
        "page_obj":page_obj
    })


@login_required
@csrf_exempt
def follow_unfollow(request, user_id):

    if request.method!= "PUT":
        return JsonResponse({"error":"PUT request is required"}, status=400)

    if request.method == "PUT":
        current_user = request.user
        profile_user = User.objects.get(pk=user_id)

        data = json.loads(request.body)
        if data.get("follow"):
            following = Following.objects.get(user = current_user, following = profile_user)
            following.delete()
            
        else:
            following = Following(user = current_user, following = profile_user)
            following.save()

        return JsonResponse({"message": "Followed successfully"}, status=201)

@login_required   
@csrf_exempt
def like(request, post_id):

    if request.method != "PUT":
        return JsonResponse({"error":"PUT request is required"}, status=400)

    if request.method == "PUT":

        try:
            current_user = request.user
            post = Post.objects.get(pk=post_id)
            data = json.loads(request.body)
            action = data.get("action")

            if action is not None:

                like, created = Like.objects.get_or_create(user=current_user, post=post)

                if action:
                    like.like = True
                else:
                    like.like = False
                like.save()

                if action:
                    post.likes += 1
                else:
                    post.likes -= 1
            
                post.save()
                return JsonResponse({"message": "success"}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        except Like.DoesNotExist:
            return JsonResponse({"error": "Like record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error":"PUT request is required"}, status=400)
    
    try:
        current_user = request.user
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)

        post.text = data["text"]
        post.save()
        return JsonResponse({"message": "success"}, status=200)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except Like.DoesNotExist:
        return JsonResponse({"error": "Like record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
