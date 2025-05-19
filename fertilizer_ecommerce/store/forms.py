from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import User

class ProfileUpdateForm(UserChangeForm):
    password = None  # Exclude password field

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
