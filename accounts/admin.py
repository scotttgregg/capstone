from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from accounts.models import User, Blog, Category

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('User info', {'fields': ('bio', 'email', 'height', 'weight', 'goals', 'profile_img')}),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Blog)
admin.site.register(Category)