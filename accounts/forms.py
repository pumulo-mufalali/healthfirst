from django.forms import ModelForm
from .models import User

class UserRegistrationForm(ModelForm):
  class Meta:
    model = User
    fields = '__all__'

class UserProfileForm(ModelForm):
  class Meta:
    model = User
    fields = '__all__'