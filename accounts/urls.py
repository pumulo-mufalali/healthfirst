from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from . import api_handlers

app_name = 'accounts'

urlpatterns = [
  path('', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),

  path('doctor_list/', views.doctor_list, name='doctor_list'),

  path('services/', views.services, name='services'),
  
  path('login/', views.loginPage, name='login'),
  path('logout/', views.userLogout, name='logout'),

  path('register/', views.register, name='register'),
  path('doctor_register/', views.doctor_register, name='doctor_register'),

  path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  
  # API endpoints for data processing
  path('api/dashboard-stats/', api_handlers.dashboard_stats_api, name='dashboard_stats_api'),
  path('api/analytics/', api_handlers.analytics_api, name='analytics_api'),
  path('api/reports/', api_handlers.report_api, name='report_api'),
  path('api/export/', api_handlers.export_api, name='export_api'),
]