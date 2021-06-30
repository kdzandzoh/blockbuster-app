from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.get_movies, name='movies'),
    path('add/', views.add_movies, name='add'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('invalid/', views.invalid, name='invalid'),
    path('my_movies/', views.my_movies, name='my_movies'),
]