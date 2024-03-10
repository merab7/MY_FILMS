from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import SignUpView, user_not_authenticated
from django.contrib.auth.decorators import login_required
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include("blog.urls")),
    path('', include("users.urls")),
    path('admin/', admin.site.urls),
    path('login/', user_not_authenticated(auth_views.LoginView.as_view(template_name='users/login.html')), name='login'),
    #prevent logged in user access register page
    path('register/', user_not_authenticated(SignUpView.as_view(template_name='users/register.html')), name='register'),
    #here i am adding login required decorator to if user is not logged in and treys to access a logout page it goes to login page first
    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='users/logout.html')), name='logout'),
    #PASSWORD RESET VIEW
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
