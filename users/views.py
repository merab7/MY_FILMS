from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, FilmSearchForm, FilmReviewForm, Post_text_form, Rank_form, Comment_form
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import FilmCard, Post, MyT_10, Comment
from django.views.generic.list import ListView
from .films_from_api import Film_data
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseRedirect




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

        return FilmCard.objects.filter(author=self.request.user).order_by('-date_created')

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
                if FilmCard.objects.filter(title=film['original_title']).exists() and FilmCard.objects.filter(year=film['release_date']).exists() :
                    messages.error(request, f'Film {film['original_title']} created in {film['release_date']} already exists in your films.')
                    return redirect('user-films')
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

            Post.objects.create(
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


class FilmFromMyFilmsDeleteView(LoginRequiredMixin,DeleteView):
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


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ["post_text"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("blog-home")



class FilmCardUpdateView(LoginRequiredMixin,UpdateView):
    model = FilmCard
    fields = ["ranking", "review"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("user-films")


class My_Top_10_listView(LoginRequiredMixin, ListView):
    model = MyT_10
    paginate_by = 4

    def get_queryset(self):
        # Filter queryset to only include films added by the current user
        queryset = MyT_10.objects.filter(author=self.request.user)
        # Order queryset by rank
        queryset = queryset.order_by('rank')
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the queryset of films for the current user
        context['my_films'] = self.get_queryset()
        return context




from django.db.models import Max

def add_to_t10(request, pk):
    film = FilmCard.objects.get(pk=pk)

    if request.method == 'POST':
        form = Rank_form(request.POST)
        if form.is_valid():
            rank = form.cleaned_data.get('rank')
            if MyT_10.objects.filter(film=film).exists():
                messages.error(request, f'{film.title} is already in top 10!')
                return redirect('user-films')

            # Calculate the maximum rank in the current user's top 10 list
            max_rank = MyT_10.objects.filter(author=request.user).aggregate(max_rank=Max('rank'))['max_rank']
            if max_rank is None:
                max_rank = 0
            
            # If the specified rank is greater than the maximum rank, adjust it
            if rank > max_rank + 1:
                rank = max_rank + 1

            # Increment the rank of conflicting films and films after the conflicting film
            conflicting_films = MyT_10.objects.filter(rank__gte=rank, author=request.user)
            for conflicting_film in conflicting_films:
                conflicting_film.rank += 1
                conflicting_film.save()
            MyT_10.objects.create(rank=rank, film=film, author=request.user)
            messages.success(request, f'Film {film.title} has been added to the TOP_10.')
            return redirect('user-t10') 

        else:
            messages.error(request, 'Please check the validity of the form and try again!')
    else:
        form = Rank_form()

    context = {
        'form': form,
        'film': film,
    }
    return render(request, 'users/rank_form.html', context)



    
def deleteT10(request, pk):
    film = MyT_10.objects.get(pk=pk)
    deleted_rank = film.rank
    film.delete() 
    for film in MyT_10.objects.filter(rank__gt=deleted_rank, author=request.user):
        film.rank -= 1
        film.save()

   
    
   

    return redirect('user-t10')






     



    


def post_author_t10(request, username):
    post_author = get_object_or_404(User, username=username)
    t10 = MyT_10.objects.filter(author=post_author)
    context = {
        't10' :t10,
        'post_author' : post_author,
    }

    print(t10)

    return render(request, 'users/authorsT10.html', context)
    

class Rank_update_view(LoginRequiredMixin, UpdateView):
    model = MyT_10
    fields = ["rank"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("user-t10")

    def form_valid(self, form):
        old_rank = self.object.rank
        new_rank = form.cleaned_data['rank']
        if old_rank != new_rank and MyT_10.objects.filter(rank=new_rank, author=self.request.user).exists():
            # Increment the rank of conflicting films
            MyT_10.objects.filter(rank__gte=new_rank, rank__lt=old_rank, author=self.request.user).update(rank=F('rank') + 1)
        return super().form_valid(form)




    


class PostDetailView(DetailView):
    model = Post
    template_name = 'users/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Comment_form()
        context['comment'] = Comment.objects.filter(post=self.get_object())
        context['comment_count'] = Comment.objects.filter(post=self.get_object()).count()
        return context
  
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = Comment_form(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            Comment.objects.create(author=request.user, post=self.object, text=comment)
            return redirect('post-detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            
            
            return render(request, self.template_name, context)



class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    def get_success_url(self):
        post_pk = self.kwargs.get('post_pk')
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})   
    

class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ["text"]
    template_name_suffix = "_update_form"

    def get_success_url(self):
        post_pk = self.kwargs.get('post_pk')
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})   
    


   