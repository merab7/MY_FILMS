from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import SignUpView, user_not_authenticated
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', include("blog.urls")),
    path('', include("users.urls")),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #prevent logged in user access register page
    path('register/', user_not_authenticated(SignUpView.as_view(template_name='users/register.html')), name='register'),
    #here i am adding login required decorator to if user is not logged in and treys to access a logout page it goes to login page first
    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='users/logout.html')), name='logout'),

]
