from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class FilmSearchForm(forms.Form):
    search = forms.CharField(label='Search')


class FilmReviewForm(forms.Form):
    rating = forms.FloatField(
        label='my_rank',
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    review = forms.CharField(
        label='Review',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False,
    )
      
     
