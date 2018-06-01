from django import forms
from accounts.models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image', 'alt_text', 'youtube', 'fitness_library']


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )
