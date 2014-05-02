from django.conf import settings
from django.core.mail import EmailMessage,  EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


def send_reply_email(request, post, form):
    subject = "Someone has replied to '%s' on %s." % (
        post.title, settings.ORGANIZATION_NAME)
    
    sender = request.user.email
    
    body = "In reference to %s, %s said:\n\n%s" % (
        request.build_absolute_uri(post.get_absolute_url()),
        sender,
        form.cleaned_data['content'])
    to = (post.contact.email,)
    headers = {'Reply-To': sender}

    email = EmailMessage(subject=subject,
                         body=body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=to,
                         headers=headers)
    try:
        email.send()
        return 1
    except:
#        logger.warn( "[send_reply_via_mail] Issue with sending email?", exc_info=True )
        return 0


def send_password_reset_url_via_email(user, reset_key):
    subject = "[%s] _(Your password reset request.)" % (settings.ORGANIZATION_NAME)    
    

    
    reset_url = "%s%s" % (settings.HOSTNAME_URL,
                          reverse('accounts_reset_password', args=[reset_key,]))
#    logger.debug( 'reset url: %r', reset_url )
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    headers = {'Reply-To': from_email}
    
    html_content = """
    <P>
    Click on the following link to reset your password.<br>
    <a HREF="%s">%s</a>
    </P>
    """ % (reset_url, reset_url)
   
    text_content="""
    Click on the following link to reset your password.
    %s
    """ % (reset_url)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        return 1
    except:
#        logger.warn( "[send_pass_reset_via_mail] Issue with sending email?", exc_info=True )
        return 0
    
def send_signup_key_via_email(user, signup_key):
    subject = "[%s] Verify your email to get started." % (settings.ORGANIZATION_NAME)    
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    headers = {'Reply-To': from_email}
    
    html_content = """
    <P>
    You're almost done.  Please click the link to activate your account.<br>
    <a HREF="%s/accounts/signup-verify/%s">%s/accounts/signup-verify/%s</a>
    </P>
    """ % (settings.HOSTNAME_URL , signup_key, settings.HOSTNAME_URL, signup_key)
   
    text_content="""
    You're almost done.  Please click the link to activate your account.
    %s/accounts/signup-verify/%
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        return 1
    except:
#        logger.warn( "[send_signup_key_via_mail] Issue with sending email?", exc_info=True )
        return 0


