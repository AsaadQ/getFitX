from django.urls import path
from . import views


urlpatterns = [
    path('boards', views.boards, name = 'boards'),
    path('boards/<int:board_id>/', views.board_topics, name='board_topics'),
    path('boards/<int:board_id>/new/', views.new_topic, name='new_topic'),
    #path('boards/<int:board_id>/new/post', views.p, name='p'),

    #path('boards/<int:board_id>/new/', views.new_topic, name='new_topic'),

]
