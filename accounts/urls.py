from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
  path('', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  
  path('login/', views.loginPage, name='login'),
  path('logout/', views.userLogout, name='logout'),

  path('register/', views.register, name='register'),
]