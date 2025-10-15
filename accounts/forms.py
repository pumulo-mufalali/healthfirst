from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 
                 'user_type', 'phone', 'address', 'profile_picture',
                 )  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserProfileForm(UserCreationForm):
  class Meta:
    model = User
    fields = '__all__'