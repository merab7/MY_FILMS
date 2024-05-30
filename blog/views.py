from django.shortcuts import render, get_object_or_404
from .models import Post, Comment , Likes
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
  
    posts = Post.objects.all().order_by('-date_created')
    post_comments_count = {}
    post_likes_count = {}
    post_is_liked = {}
    post_like_authors = {}
    for post in posts:
        post_comments_count[post.pk] = Comment.objects.filter(post=post).count()
        post_likes_count[post.pk] = Likes.objects.filter(post=post).count()
        if request.user.is_authenticated:
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




def like_post(request, pk):
    if not request.user.is_authenticated:
        login_url = reverse('login')
        return JsonResponse({'redirect': login_url}, status=401)

    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if Likes.objects.filter(post=post, author=user).exists():
        Likes.objects.filter(post=post, author=user).get().delete()
        is_liked = False
    else:
        Likes.objects.create(post=post, author=user)
        is_liked = True

    likes_count = Likes.objects.filter(post=post).count()
    response = {
        'is_liked': is_liked,
        'likes_count': likes_count,
    }

    return JsonResponse(response)

@login_required
def get_likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes = Likes.objects.filter(post=post)
    usernames = [like.author.username for like in likes]
    return JsonResponse({'usernames': usernames})