from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, FilmSearchForm, FilmReviewForm, Post_text_form
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import FilmCard, Post
from django.views.generic.list import ListView
from .films_from_api import Film_data
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.models import User



#this decorator prevents signed users form accessing the register page 
#it checks if the user is authenticated and if it is sends it to home page 
#else allows user to access register page
#i am using this function in project's main url 
def user_not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog-home')  # Redirect to the home page if the user is logged in
        return view_func(request, *args, **kwargs)
    return wrapper


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url= reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = 'Your profile was created successfully'

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"{request.user.username} Your profile has been updated.")
            return redirect('users-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form, 
    }


    return render(request, 'users/profile.html', context)



class FilmListView(LoginRequiredMixin, ListView):
    model = FilmCard
    paginate_by = 4  # if pagination is desired

    def get_queryset(self):
        form = FilmSearchForm(self.request.GET)
        data = Film_data()

        if form.is_valid():
            self.film_name = form.cleaned_data.get('search')
            self.film_options = data.find_film(self.film_name)
        else:
            self.film_options = []

        return FilmCard.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = getattr(self, 'form', FilmSearchForm())  # Add the form to the context
        context['film_options'] = getattr(self, 'film_options', [])  # Add film_options to the context
        context['film_name'] = getattr(self, 'film_name', '')
        return context
    




def add_to_my_films(request, id):
    data = Film_data()
    film_id = id  
    film = data.find_with_id(film_id)
    MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

    if film:
        if request.method == 'POST':
            form = FilmReviewForm(request.POST)
            if form.is_valid():
                film_to_add = FilmCard(
                    title=film['original_title'],
                    year=film['release_date'],
                    description=film['overview'],
                    rating=film['vote_average'],
                    ranking=form.cleaned_data['rating'],
                    review=form.cleaned_data['review'],
                    img_url=f"{MOVIE_DB_IMAGE_URL}{film['poster_path']}",
                    author=request.user,
                    
                )

                film_to_add.save()
                messages.success(request, 'The film has been added with your review and rating')
                return redirect('user-films')
        else:
            form = FilmReviewForm()

        context = {
            'form': form,
            'film': film,
        }

        return render(request, 'users/review_ranking.html', context)

    messages.error(request, 'Film not found')
    return redirect('user-films')


def post_film(request, pk):
    film = FilmCard.objects.get(pk=pk)

    if request.method == 'POST':
        form = Post_text_form(request.POST)  # Create an instance of the form
        if form.is_valid():
            post_text = form.cleaned_data['post_text']
            author = request.user

            post = Post.objects.create(
                post_text=post_text,
                film=film,
                author=author,
            )

            messages.success(request, 'Your post has been added to the home page!')
            return redirect('blog-home')
    else:
        form = Post_text_form()

    context = {'form': form}
    return render(request, 'users/post_text.html', context)


class FilmFromMyFilmsDeleteView(DeleteView):
    model = FilmCard
    success_url = reverse_lazy("user-films")
       
   
    
   
def user_posts(request, username):
    post_author_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=post_author_user)
    context = {
        'posts' : posts,
        'post_author_user' : post_author_user,
    }
    
    return render(request, 'users/users_posts.html', context)


class PostUpdateView(UpdateView):
    model = Post
    fields = ["post_text"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("blog-home")



class FilmCardUpdateView(UpdateView):
    model = FilmCard
    fields = ["ranking", "review"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("user-films")






    


