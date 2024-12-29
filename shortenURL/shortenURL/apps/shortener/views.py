from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import ShortenedURL, URLAccess

class URLStatsManager:
    
    @staticmethod
    def get_url_stats(url, include_recent=False):
        stats = {
            'total_clicks': url.accesses.count(),
            'unique_ips': url.accesses.values('ip_address').distinct().count(),
            'last_accessed': url.accesses.order_by('-accessed_at').first()
        }
        if include_recent:
            stats['recent_accesses'] = url.accesses.order_by('-accessed_at')[:10]
        return stats

    @classmethod
    def get_urls_with_stats(cls, urls):
        return [{
            'url': url,
            'stats': cls.get_url_stats(url)
        } for url in urls]

@method_decorator(login_required, name='dispatch')
class URLCreateView(View):
    template_name = 'shortener/create_url.html'

    def get_recent_urls(self):
        user_urls = ShortenedURL.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:5]
        return URLStatsManager.get_urls_with_stats(user_urls)

    def get(self, request):
        return render(request, self.template_name, {
            'urls_with_stats': self.get_recent_urls()
        })

    def post(self, request):
        original_url = request.POST.get('url')
        if not original_url:
            return redirect('create_url')

        short_code = ShortenedURL.generate_short_code()
        shortened_url = ShortenedURL.objects.create(
            user=request.user,
            original_url=original_url,
            short_code=short_code
        )

        return render(request, self.template_name, {
            'shortened_url': request.build_absolute_uri(f'/s/{short_code}'),
            'original_url': original_url,
            'urls_with_stats': self.get_recent_urls()
        })

class URLRedirectView(View):
    def get(self, request, short_code):
        shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
        
        URLAccess.objects.create(
            shortened_url=shortened_url,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            referrer=request.META.get('HTTP_REFERER')
        )
        
        return redirect(shortened_url.original_url)

@method_decorator(login_required, name='dispatch')
class URLStatsView(View):
    template_name = 'shortener/url_stats.html'

    def get(self, request, short_code):
        url = get_object_or_404(
            ShortenedURL, 
            short_code=short_code, 
            user=request.user
        )
        
        stats = URLStatsManager.get_url_stats(url, include_recent=True)
        
        return render(request, self.template_name, {
            'url': url,
            'stats': stats
        })

@method_decorator(login_required, name='dispatch')
class URLListView(View):
    template_name = 'shortener/url_list.html'

    def get(self, request):
        user_urls = ShortenedURL.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        urls_with_stats = URLStatsManager.get_urls_with_stats(user_urls)
        
        return render(request, self.template_name, {
            'urls_with_stats': urls_with_stats
        })