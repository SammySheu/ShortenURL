from django.shortcuts import render
from django.views.generic import TemplateView
from allauth.account.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging

logger = logging.getLogger('accounts')  # 使用你配置的 logger

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User logged in - Email: {user.email}")
    logger.info(f"Next URL: {request.GET.get('next', '/')}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        logger.info(f"User logged out - Email: {user.email}")

class LoginView(TemplateView):
    template_name = "login.html"
