from django.urls import path
from . import views


urlpatterns = [
    path('valg', views.valg, name='val'),#dette het calc
    path('Basic', views.Basic_work, name='basic'),  # dette het calc
    path('Hard', views.Basic_hard, name='hard'),  # dette het calc
    path('Ultra', views.Basic_ultra, name='ultra'),  # dette het calc
]