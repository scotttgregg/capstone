from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from accounts.models import User, Blog, Category, ShopItem
from martor.widgets import AdminMartorWidget
from django.db import models


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('User info', {'fields': ('bio', 'email', 'height', 'weight', 'goals', 'profile_img')}),
    )


class BlogModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(User, MyUserAdmin)
admin.site.register(Blog, BlogModelAdmin)
admin.site.register(Category)
admin.site.register(ShopItem)