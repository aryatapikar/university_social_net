from django.urls import path
from . import views

app_name = 'user_profs'

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/', views.delete, name='delete'),
    path('edit/', views.go_to_edit, name='edit'),
    path('save_edit/', views.save_edit, name='save_edit'),
]