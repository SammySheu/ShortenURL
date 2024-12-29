"""
URL configuration for shortenURL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .apps.accounts.views import LoginView
from .apps.shortener.views import (
    URLCreateView, URLRedirectView, 
    URLStatsView, URLListView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path('', URLCreateView.as_view(), name='create_url'),
    path('s/<str:short_code>/', URLRedirectView.as_view(), name='redirect_url'),
    path('stats/<str:short_code>/', URLStatsView.as_view(), name='url_stats'),
    path('my-urls/', URLListView.as_view(), name='url_list'),
    # path('shorten_url/', create_short_url, name='create_short_url'),
]
