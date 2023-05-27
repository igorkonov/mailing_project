from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from users.models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
        field_classes = {"username": UsernameField}
