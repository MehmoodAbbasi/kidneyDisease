from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import * 

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Create a strong password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'role')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

