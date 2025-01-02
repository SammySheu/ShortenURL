# shortenURL/apps/accounts/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os

class Command(BaseCommand):
    help = 'Setup initial users and social authentication'

    def handle(self, *args, **kwargs):
        self.setup_superuser()
        self.setup_site()
        self.setup_social_apps()

    def setup_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created successfully')
            )

    def setup_site(self):
        site = Site.objects.get(id=1)
        site.domain = '127.0.0.1:8000'
        site.name = 'ShortenURL'
        site.save()
        self.stdout.write(
            self.style.SUCCESS('Site configured successfully')
        )

    def setup_social_apps(self):
        site = Site.objects.get(id=1)

        # Setup Google
        if not SocialApp.objects.filter(provider='google').exists():
            google_app = SocialApp.objects.create(
                provider='google',
                name='Google OAuth2',
                client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
                secret=os.getenv('GOOGLE_CLIENT_SECRET', '')
            )
            google_app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS('Google OAuth2 configured')
            )

        # Setup Facebook
        if not SocialApp.objects.filter(provider='facebook').exists():
            facebook_app = SocialApp.objects.create(
                provider='facebook',
                name='Facebook OAuth2',
                client_id=os.getenv('FACEBOOK_CLIENT_ID', ''),
                secret=os.getenv('FACEBOOK_CLIENT_SECRET', '')
            )
            facebook_app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS('Facebook OAuth2 configured')
            )
        
        # Setup Github
        if not SocialApp.objects.filter(provider='github').exists():
            github_app = SocialApp.objects.create(
                provider='github',
                name='Github OAuth2',
                client_id=os.getenv('GITHUB_CLIENT_ID', ''),
                secret=os.getenv('GITHUB_CLIENT_SECRET', '')
            )
            github_app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS('Github OAuth2 configured')
            )