
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

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User 
from datetime import date, datetime, timedelta
from emails import send_password_reset_url_via_email, send_signup_key_via_email
import uuid

from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict


       
class ValidPasswordResetKey(models.Model):
    user               = models.ForeignKey(User)
    reset_password_key = models.CharField(max_length=50, blank=True)
    expires            = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        if self.reset_password_key is not None:
            return '%s for user %s expires at %s' % (self.reset_password_key,
                                                 self.user.username,
                                                 self.expires)
        else:
            return None
        
    def save(self, **kwargs):
        
        self.reset_password_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(days=settings.DAYS_TO_REGISTER)
        self.expires=expires
        
        #send an email with reset url
        x=send_password_reset_url_via_email(self.user, self.reset_password_key)
        if x:
            super(ValidPasswordResetKey, self).save(**kwargs)
        else:
            self.reset_password_key=None 


class ValidSignupKey(models.Model):
    user                 = models.ForeignKey(User)
    signup_key           = models.CharField(max_length=50, blank=True,
                                            unique=True)
    expires              = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.signup_key,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        
        self.signup_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(days=settings.DAYS_TO_REGISTER)
        self.expires=expires
        
        #send an email with reset url
        x=send_signup_key_via_email(self.user, self.signup_key)
        super(ValidSignupKey, self).save(**kwargs)

              
def validate_signup(signup_key):
    try:
        vc=ValidSignupKey.objects.get(signup_key=signup_key)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False   
    except(ValidSignupKey.DoesNotExist):
        return False  
    u=vc.user
    u.is_active=True
    u.save()
    vc.delete()
    return True
