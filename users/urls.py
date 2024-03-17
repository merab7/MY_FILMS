from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.profile, name="users-profile"),
    path('add_to_films/<int:id>/', views.add_to_my_films, name='add_film'),
    path('post-film/<pk>/', views.post_film, name='post-film'),
    path('user-posts/<username>', views.user_posts, name='user-posts'),
    path('post_author_t10/<username>', views.post_author_t10, name='post_author_t10'),
    path('rank_film/<pk>', views.add_to_t10, name='add_to_t10')
]