from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="blog-home"),
    path('like/<int:pk>/', views.like_post, name='like-post'),
]