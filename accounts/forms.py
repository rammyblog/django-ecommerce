from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class Register(UserCreationForm):
	first_name= forms.CharField(max_length = 50,)
	last_name= forms.CharField(max_length = 50,)
	email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address')
	class Meta:
		model = User
		fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['user','first_name', 'last_name', 'address','additional_info', 'phone', 'phone2', 'city', ]
