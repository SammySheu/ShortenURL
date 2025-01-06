from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
from django.views.generic import TemplateView
from allauth.account.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings
import logging

logger = logging.getLogger('accounts')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user=user)
        provider = social_account.provider
    except SocialAccount.DoesNotExist:
        provider = "direct login"

    logger.info(f"User logged in - ID: {user.id}, "
                f"Email: {user.email}, "
                f"Username: {user.username}, "
                f"Provider: {social_account.provider}, "
                f"Response Status: {request.META.get('HTTP_STATUS', 'N/A')}")
    logger.info(f"Request Headers: {request.headers}")
    logger.info(f"Redirect URL from settings: {settings.LOGIN_REDIRECT_URL}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        logger.info(f"User logged out - Email: {user.email}")

class LoginView(TemplateView):
    template_name = "login.html"
