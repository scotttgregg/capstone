from django.urls import path, include
from accounts import views
from django.contrib.auth.views import login, logout

urlpatterns = [

    path('blog/', views.blog, name='blog_home'),
    path('blog/<slug:cat>/<slug:slug>/', views.blog_single_view, name='blog_single_view'),
    path('blog/blog_create', views.blog_create, name='blog_create'),
    path('login/', login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', logout, name='logout'),
    path('fitness_library/', views.fitness_library, name='fit_lib'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('martor/', include('martor.urls')),

]