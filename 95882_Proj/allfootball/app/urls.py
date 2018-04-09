from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('topics/', views.TopicListView.as_view(), name='topics'),
    path('own_topics/', views.OwnTopicListView.as_view(), name='own_topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('redirect_login/', views.to_login, name='redirect_login'),
    re_path(r'(?P<pk>[-\w]+)/$', views.TopicDetailView.as_view(), name='topic_detail'),
]