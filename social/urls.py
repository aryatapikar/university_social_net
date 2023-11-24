from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('add_post/', views.add_post, name='add_post'),
    path('comment', views.comment, name='comment'),
]