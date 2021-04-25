from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),  # get dashboard
    url(r'^workout$', views.ny_Trening),  # get workout page / add workout
    url(r'^workout/(?P<id>\d*)$', views.workout, name='workout'),  # get workout / update workout
    url(r'^workout/(?P<id>\d*)/exercise$', views.exercise),  # add exercise
    url(r'^workout/(?P<id>\d*)/complete$', views.complete_workout),  # complete workout
    url(r'^workout/(?P<id>\d*)/edit$', views.edit_workout),  # edit workout
    url(r'^workout/(?P<id>\d*)/delete$', views.delete_workout),  # delete workout
    url(r'^workouts$', views.alle_Trening),  # get all workouts
]
