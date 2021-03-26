from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', views.user_register, name='user_register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("user", views.userpage, name = "userpage"),
    path("workouts", views.all_workouts, name= "workouts"),
]