from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ShortenedURL, URLAccess

# Create your views here.

@login_required
def create_short_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        if not original_url:
            return JsonResponse({'error': 'URL is required'}, status=400)
            
        short_code = ShortenedURL.generate_short_code()
        shortened_url = ShortenedURL.objects.create(
            user=request.user,
            original_url=original_url,
            short_code=short_code
        )
        
        return render(request, 'shortener/create_url.html', {
            'shortened_url': request.build_absolute_uri(f'/s/{short_code}'),
            'original_url': original_url
        })
        
    return render(request, 'shortener/create_url.html')

def redirect_url(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    
    # 記錄訪問資訊
    URLAccess.objects.create(
        url=shortened_url,
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