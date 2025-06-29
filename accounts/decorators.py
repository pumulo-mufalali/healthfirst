from django.http import HttpResponse
from django.shortcuts import redirect

def unauthorized_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('/')
    else:
      return view_func(request, *args, **kwargs)
  return wrapper_func

def allowed_user(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = ''
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name
      if group in allowed_roles:
        return view_func(request, *args, **kwargs)
      else: 
        return redirect('login')
    return wrapper_func
  return decorator


def admin_only(view_func):
  def wrapper_func(request, *args, **kwargs):
    group = None
    if request.user.groups.exists():
      group = request.user.groups.all()[0].name

    if group == 'admin':
      return view_func(request, *args, **kwargs)
    else:
      return redirect('home')
    
  return wrapper_func