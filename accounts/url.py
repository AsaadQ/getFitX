from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views

from .views import PasswordChangeView

urlpatterns = [
    path('signup', views.user_register, name='user_register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("user", views.userpage, name = "userpage"),
    path('password/', PasswordChangeView.as_view(template_name='Bruker/ByttePassword.html'), name='password'),
    path('password_Endret', views.password_Endret, name='password_Endret'),
]