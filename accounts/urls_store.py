from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.store, name='store'),
    path('store_create/', views.store_create, name='store_create'),
    path('store_single_view/<slug:slug>/', views.store_single_view, name='store_single_view'),
]
