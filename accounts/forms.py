from django import forms
from accounts.models import Blog, User
from django.contrib.auth.forms import UserCreationForm


class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image', 'alt_text', 'youtube', 'fitness_library']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
