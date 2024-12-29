from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ShortenedURL, URLAccess

# Create your views here.

@login_required
def create_short_url(request):
    # Get user's URLs with stats
    user_urls = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')[:5]  # Show last 5 URLs
    urls_with_stats = []
    
    for url in user_urls:
        stats = {
            'total_clicks': url.accesses.count(),
            'unique_ips': url.accesses.values('ip_address').distinct().count(),
            'last_accessed': url.accesses.order_by('-accessed_at').first()
        }
        urls_with_stats.append({
            'url': url,
            'stats': stats
        })

    if request.method == 'POST':
        original_url = request.POST.get('url')
        if original_url:
            short_code = ShortenedURL.generate_short_code()
            shortened_url = ShortenedURL.objects.create(
                user=request.user,
                original_url=original_url,
                short_code=short_code
            )
            return render(request, 'shortener/create_url.html', {
                'shortened_url': request.build_absolute_uri(f'/s/{short_code}'),
                'original_url': original_url,
                'urls_with_stats': urls_with_stats
            })
    
    return render(request, 'shortener/create_url.html', {
        'urls_with_stats': urls_with_stats
    })

def redirect_url(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    
    # 記錄訪問資訊
    URLAccess.objects.create(
        shortened_url=shortened_url,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        referrer=request.META.get('HTTP_REFERER')
    )
    
    return redirect(shortened_url.original_url)

@login_required
def url_stats(request, short_code):
    url = get_object_or_404(ShortenedURL, short_code=short_code, user=request.user)
    
    stats = {
        'total_clicks': url.accesses.count(),
        'unique_ips': url.accesses.values('ip_address').distinct().count(),
        'recent_accesses': url.accesses.order_by('-accessed_at')[:10]
    }
    
    return render(request, 'shortener/url_stats.html', {
        'url': url,
        'stats': stats
    })

@login_required
def url_list(request):
    user_urls = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')
    
    urls_with_stats = []
    for url in user_urls:
        stats = {
            'total_clicks': url.accesses.count(),  # Use the new related_name
            'unique_ips': url.accesses.values('ip_address').distinct().count(),
            'last_accessed': url.accesses.order_by('-accessed_at').first()
        }
        urls_with_stats.append({
            'url': url,
            'stats': stats
        })
    
    return render(request, 'shortener/url_list.html', {
        'urls_with_stats': urls_with_stats
    })