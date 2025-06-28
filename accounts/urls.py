from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  
  path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),

  path('register/', views.register, name='register'),
  path('user_login/', views.user_login, name='user_login'),
  path('user_logout/', views.user_logout, name='user_logout'),
  path('profile/', views.profile, name='profile'),
]