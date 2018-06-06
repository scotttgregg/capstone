from django import forms
from accounts.models import Blog, User, ShopItem
from django.contrib.auth.forms import UserCreationForm


class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image', 'alt_text', 'youtube', 'fitness_library']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ShopItemForm(forms.ModelForm):
    class Meta:
        model = ShopItem
        fields = ['product_name', 'file', 'img', 'alt_text', 'short_description', 'description', 'price']
