from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def profile_img_uh(instance, filename):
    return 'users/{}/img/{}'.format(instance.username, filename)


class User(AbstractUser):
    # username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField()
    email = models.CharField(max_length=30)
    height = models.CharField(max_length=30, blank=True)
    weight = models.CharField(max_length=30, blank=True)
    goals = models.CharField(max_length=500, blank=True)
    profile_img = models.ImageField(upload_to=profile_img_uh, blank=True, null=True)

    # alt_text = models.CharField(max_length=255, blank=True, null=True)
    # file = models.ImageField(upload_to=profile_img_uh)
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='images')
    # description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.first_name


def blog_image_uh(instance, filename):
    return 'blog/{}/blog_image/{}'.format(instance.author, filename)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey('Category', default=1, related_name='blogs', on_delete=models.SET_DEFAULT)
    image = models.ImageField(upload_to=blog_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=30, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    fitness_library = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Blog.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)

    class Meta:
        ordering = ['-pk']


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.name)
            checking = True
            while checking:
                results = Category.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
            super().save(args, kwargs)

    class Meta:
        verbose_name_plural = 'Categories'



def product_img_uh(instance, filename):
    return 'products/{}/{}'.format(instance.product_name, filename)


class ShopItem(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True)
    product_name = models.CharField(max_length=50)
    file = models.FileField(null=True)
    img = models.ImageField(upload_to=product_img_uh, null=True)
    alt_text = models.CharField(max_length=50, null=True)
    short_description = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500)
    price = models.CharField(max_length=50, null=True)
    store_button = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.product_name)
            checking = True
            while checking:
                results = ShopItem.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.product_name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


class BuyerResponse(models.Model):
    email = models.CharField(max_length=50)
    date = models.




