from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import SignUpView, user_not_authenticated, FilmListView, \
                        FilmFromMyFilmsDeleteView, PostUpdateView, \
                        FilmCardUpdateView, My_Top_10_listView, T10_DeleteView, Rank_update_view, PostDetailView, \
                        CommentDeleteView, CommentUpdateView
from blog.views import PostDeleteView
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
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete'),
    #FILMS
    path('my-films/', login_required( FilmListView.as_view(template_name = "users/filmCard_list.html")), name='user-films'),
    path('delete-film/<pk>', login_required(FilmFromMyFilmsDeleteView.as_view(template_name = "users/filmCard_confirm_delete.html")), name='delete-film'),
    path('delete-post/<pk>', login_required(PostDeleteView.as_view(template_name = "blog/filmCard_confirm_delete.html")), name='delete-post'),
    path('edit-post/<pk>', login_required(PostUpdateView.as_view(template_name = "users/post_update_form.html")), name='update-post'),
    path('edit-filmCard/<pk>', login_required(FilmCardUpdateView.as_view(template_name = "users/filmCard_update_form.html")), name='update-filmCard'),
    #t10
    path('my-top10/',login_required( My_Top_10_listView.as_view(template_name = "users/myT_10_list.html")), name='user-t10'),
    path('pop/<pk>', login_required( T10_DeleteView.as_view(template_name = "users/myT_10_confirm_delete.html")), name='t10-delete'),
    path('edit-ranking/<pk>', login_required(Rank_update_view.as_view(template_name = "users/myT_10_update_form.html")), name='update-rank'),
    #post_details
    path("post-details/<pk>", PostDetailView.as_view(template_name = "users/post_detail.html"), name="post-detail"),
    #comments
    path('delete-comment/<post_pk>/<pk>', login_required(CommentDeleteView.as_view(template_name = "users/comment_confirm_delete.html")), name='comment-delete'),
    path('update-comment/<post_pk>/<pk>', login_required(CommentUpdateView.as_view(template_name = "users/comment_update_form.html")), name='comment-update'),
  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
