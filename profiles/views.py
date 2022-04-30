from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import models


# Create your views here.


def signup(request):
    if request.POST:
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserSignUpForm()

    return render(request, "profiles/signup.html", {"form": form})


def signin(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if "@" in username:
                user_object = User.objects.get(email=username)
                username = user_object.username
        except:
            pass

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("success")
    else:
        form = AuthenticationForm()

    return render(request, "profiles/signin.html", {"form": form})


def index(request):
    # quires are executed lazily
    latest_articles = models.Article.objects.all().order_by('-createAT')[:10]
    context = {
        "latest_articles": latest_articles
    }
    return render(request, 'blog/index.html', context)


def article(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    context = {
        "article": article
    }
    return render(request, 'blog/article.html', context)


def author(request, pk):
    author = get_object_or_404(models.Author, pk=pk)
    context = {
        "author": author
    }
    return render(request, 'blog/author.html', context)


def create_article(request):
    authors = models.Author.objects.all()
    context = {
        "authors": authors
    }
    if request.method == "POST":
        article_data = {
            'title': request.POST['title'],
            'content': request.POST['content']
        }

        article = models.Article.objects.create(**article_data)
        author = models.Author.objects.get(pk=request.POST['author'])
        article.authors.set([author])
        context["success"] = True

    return render(request, 'blog/create_article.html', context)
