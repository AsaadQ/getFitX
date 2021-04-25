from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='khara'), #dette het home
    path('kalori', views.calc, name='home'),#dette het calc
]