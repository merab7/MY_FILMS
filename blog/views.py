from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment , Likes
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView




def home(request):
  
    posts = Post.objects.all().order_by('-date_created')
    post_comments_count = {}
    post_likes_count = {}
    post_is_liked = {}
    post_like_authors = {}
    for post in posts:
        post_comments_count[post.pk] = Comment.objects.filter(post=post).count()
        post_likes_count[post.pk] = Likes.objects.filter(post=post).count()
        post_is_liked[post.pk] = Likes.objects.filter(post=post, author=request.user).exists()
        post_like_authors[post.pk] = ', '.join(like.author.username for like in Likes.objects.filter(post=post))

    context = {
        'posts': posts,
        'post_comment_count' : post_comments_count,
        'post_likes_count' : post_likes_count,
        'post_is_liked' : post_is_liked,
        'post_like_authors' : post_like_authors
    }
    return render(request, 'blog/home.html', context)



class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog-home")


from django.http import JsonResponse

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if Likes.objects.filter(post=post, author=user).exists():
        Likes.objects.filter(post=post, author=user).get().delete()
        is_liked = False
    else:
        Likes.objects.create(post=post, author=user)
        is_liked = True

    response = {
        'is_liked': is_liked,
        'likes_count': Likes.objects.filter(post=post).count(),
    }

    return JsonResponse(response)
  