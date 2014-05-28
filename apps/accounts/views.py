
import json
from datetime import datetime

from django.http import (HttpResponseRedirect, HttpResponse,
                         HttpResponseServerError)
from django.shortcuts import (render_to_response,
                              get_object_or_404,
                              get_list_or_404)
from django.conf import settings
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from models import *
from forms import (LoginForm, RegisterForm,
                   PasswordResetForm,
                   PasswordResetRequestForm,
                   ChangePasswordForm)


def accounts_register(request):
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            pw = request.POST['password1']
            new_user = register_form.save()
            user = authenticate(username=new_user.username, password=pw)
            login(request, user)
            return HttpResponseRedirect('/publications')
        else:
            return render_to_response('accounts/register.html',
                                      RequestContext(request,
                                                     {'form': register_form,
                                                     }))
    #this is an HTTP  GET
    return render_to_response('accounts/register.html',
                              RequestContext(request,
                             {'form': RegisterForm()}))
            
def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
          new_user = form.save()
          messages.success(request, _("Please check your email to verify your account before logging in."))
          return HttpResponseRedirect(reverse('accounts_login'))
        else:
            return render_to_response('accounts/register.html',
                                      RequestContext(request, {'form': form}))      

    #this is an HTTP  GET
    return render_to_response('accounts/register.html',
                              RequestContext(request,
                             {'form': RegisterForm()}))
                   

def accounts_logout(request):
    logout(request)
    msg = _("You have logged out successfully.")
    #if request.is_ajax:
    #    #AJAX
    #    msg = {"message": msg}
    #    return HttpResponse(json.dumps(msg), mimetype="application/json")
    #messages.success(request, msg)
    return HttpResponseRedirect(reverse('home'))


def accounts_login(request):
    
    if request.method == 'POST':
        next = request.GET.get('next','')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            login(request,user)
            msg = _("You have logged in successfully.")
            if next and next != "/accounts/login/":
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/publications')
        else:
            return render_to_response('accounts/login.html',
                                      RequestContext(request,
                                                     {'login_form': login_form,
                                                     }))

    #this is a GET
    return render_to_response('accounts/login.html',
                              {'login_form': LoginForm()},
                              context_instance = RequestContext(request))


def reset_password(request, reset_password_key=None):
    
    try:
        vprk=ValidPasswordResetKey.objects.get(
                                        reset_password_key=reset_password_key)    
    except:
        msg = _("The password reset key is invalid")
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('accounts_login'))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            msg = _("Your password has been reset. Please login with your new password.")
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('accounts_login'))            
        else:
            return render_to_response('accounts/reset-password.html',
                                      RequestContext(request,
                                    {'form': form,
                                     'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))
        

def request_new_password(request):

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            a_user=User.objects.get(email=data['email'])
            a_key=ValidPasswordResetKey.objects.create(user=a_user)
            msg = _("An email to reset your password has been sent to %s. Please check your email.") % (a_user.email)
            if a_key.reset_password_key is not None:
                messages.success(request, msg)
                return HttpResponseRedirect(reverse('accounts_login'))
            else:
                msg = _("System unavailable, please try later.")
                messages.error(request, msg) 
    
        #the form contained errors
        return render_to_response('accounts/request-new-password.html', 
                             {'form': form},
                              context_instance = RequestContext(request))

    return render_to_response('accounts/request-new-password.html', 
                             {'form': PasswordResetRequestForm()},
                              context_instance = RequestContext(request))


def verify_email(request, verification_key,
                 template_name='accounts/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                              context_instance=context)

"""
def signup_verify(request, signup_key=None):
    
    if validate_signup(signup_key=signup_key):
        messages.success(request, _("Your account has been activated. You may now login."))
        return HttpResponseRedirect(reverse('accounts_login'))
    else:
        return render_to_response('accounts/invalid-signup-key.html',
                              RequestContext(request,
                                             {}))
"""

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            messages.success(request, _("Your password has been changed."))
            return HttpResponseRedirect(reverse('home'))
            
        else:
            messages.error(request, _("Oops. Something went wrong."))
            return render_to_response('accounts/change-password.html',
                              RequestContext(request, {'form': form}))
    #this is a GET
    return render_to_response('accounts/change-password.html',
                              {'form': ChangePasswordForm()},
                              context_instance = RequestContext(request))


