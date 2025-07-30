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

  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]