
"""
Copyright (C) 2012  University of Miami
 
This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
 See the GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from django import forms
from  models import *
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class PasswordResetRequestForm(forms.Form):
    email= forms.EmailField(max_length=75, label=_("Email"))
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).count() == 0:
            raise forms.ValidationError("We don't have your E-Mail registered.")
        return email    
    
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password*"))
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Confirm Password*"))

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("Please check that your passwords match and try again."))
        if len(password1) < settings.PASSWORD_MINIMUM_LENGTH:
            msg=_("Password must be at least %s characters long.") % (settings.PASSWORD_MINIMUM_LENGTH)
            raise forms.ValidationError(msg)
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("Username"))
    password = forms.CharField(widget=forms.PasswordInput, max_length=30,
                               label=_("Password"))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user=authenticate(username=username, password=password)
        if user and user.check_password(password):
            if not user.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(
                _("There was an error with your Username/Password combination. Please try again."))

        return cleaned_data



class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Confirm Password"))
    

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) < settings.PASSWORD_MINIMUM_LENGTH:
            msg=_("Password must be at least %s characters long. ") % (settings.PASSWORD_MINIMUM_LENGTH)
            raise forms.ValidationError(msg)
        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data["password2"]
        if len(password2) < settings.PASSWORD_MINIMUM_LENGTH:
            msg=_("Password must be at least %s characters long. ") % (settings.PASSWORD_MINIMUM_LENGTH)
            raise forms.ValidationError(msg)
        return password2
    
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(_("Please check that your passwords match and try again."))
        return cleaned_data
   



class RegisterForm(forms.Form):
    
    username                = forms.CharField(max_length=30, label=_("Username"))
    email                   = forms.EmailField(max_length=150, label=_("Email Address"))
    first_name              = forms.CharField(max_length=100, label=_("First Name"))
    last_name               = forms.CharField(max_length=100, label=_("Last Name"))
    password1               = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password"))
    password2               = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Confirm Password"))
 
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("Please check that your passwords match and try again."))
        if len(password1) < settings.PASSWORD_MINIMUM_LENGTH:
            msg=_("Password must be at least %s characters long. ") % (settings.PASSWORD_MINIMUM_LENGTH)
            raise forms.ValidationError(msg)
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email', "")
        if email:
            if email and User.objects.filter(email=email).count():
                raise forms.ValidationError(_("We're sorry. That email address is already registered. Please use another email address."))
            return email.lower()
        else:
            return email.lower()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).count()>0:
            raise forms.ValidationError(_("We're sorry. That username is already taken. Please choose another username."))
        return username.lower()
    


    def save(self):
        new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'],
                        )
        
        new_user.is_active = True
        new_user.save()
        #send the email verification
        #v=ValidSignupKey(user=new_user)
        #v.save()
        
        return new_user
