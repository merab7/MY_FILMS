from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages



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


