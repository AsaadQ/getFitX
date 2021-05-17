from django.urls import path
from . import views


urlpatterns = [
    path('Plans', views.Planner, name='Plans'),
    path('Over', views.Over, name='over'),
]