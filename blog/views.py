from django.shortcuts import render
from .models import Post
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView



def home(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)



class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog-home")
