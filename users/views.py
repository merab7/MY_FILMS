from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, FilmSearchForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import FilmCard
from django.views.generic.list import ListView
from .films_from_api import Film_data
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin






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
    paginate_by = 5  # if pagination is desired

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
    


from django.contrib import messages

def add_to_my_films(request, id):
    data = Film_data()
    film_id = id  
    film = data.find_with_id(film_id)
    MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

    if film:
        film_to_add = FilmCard(
            title=film['original_title'],
            year=film['release_date'],
            description=film['overview'],
            rating=film['vote_average'],
            ranking=0,  
            review="",  
            img_url=f"{MOVIE_DB_IMAGE_URL}{film['poster_path']}",
            author = request.user
        )

        film_to_add.save()
        messages.success(request, 'The film has been added')

    return redirect('user-films')  




    





    


