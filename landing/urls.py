from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.login, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]