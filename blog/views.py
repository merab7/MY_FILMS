from django.shortcuts import render
from .models import Post
from django.http import HttpResponse


def home(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)
