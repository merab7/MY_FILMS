from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.profile, name="users-profile"),
    path('add_to_films/<int:id>/', views.add_to_my_films, name='add_film')
]