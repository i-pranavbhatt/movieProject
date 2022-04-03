from dataclasses import field

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Client, Customer
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields =  ['username','email','password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class mypasswordchangeform(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label='New password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New  password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields = ['c_name','c_locality','c_city','c_zipcode']
        widgets = {'c_name':forms.TextInput(attrs={'class':'form-control'}),
                   'c_locality':forms.TextInput(attrs={'class':'form-control'}),
                   'c_city':forms.TextInput(attrs={'class':'form-control'}),
                   'c_zipcode':forms.TextInput(attrs={'class':'form-control'})}



