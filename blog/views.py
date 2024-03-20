from django.shortcuts import render
from .models import Post, Comment 
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView



def home(request):
    posts = Post.objects.all().order_by('-date_created')
    comments = Comment.objects.all()
    context = {
        'posts': posts,
        'comments': comments
    }
    return render(request, 'blog/home.html', context)



class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog-home")
