from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Blog, Category, ProfileImage




admin.site.register(User, UserAdmin)
admin.site.register(ProfileImage)
admin.site.register(Blog)
admin.site.register(Category)