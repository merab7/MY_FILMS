from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="blog-home"),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('get-likes/<int:post_id>/', views.get_likes, name='get_likes'),
]