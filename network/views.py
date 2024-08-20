import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Like, Post, Following


def index(request):
    posts = Post.objects.all().order_by('-id')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page.
        page_obj = p.page(1)
    except EmptyPage:
        # If page_number is out of range (e.g., 9999), deliver the last page of results.
        page_obj = p.page(p.num_pages)

    return render(request, "network/index.html", {
        "posts":page_obj,
        "page_obj":page_obj
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
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user)
    return render(request, 'network/profile.html', {
        "profile":user,
        "posts":posts,
    })
