from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class RegisterForm(UserCreationForm):
#     username = forms.CharField(max_length=50)
#     asal_negara = forms.CharField(max_length=50)

#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'asal_negara')