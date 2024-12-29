from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.
class ShortenedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def generate_short_code(cls):
        # 生成短網址代碼
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(6))
            if not cls.objects.filter(short_code=short_code).exists():
                return short_code

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class URLAccess(models.Model):
    url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='accesses')
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.url.short_code} accessed from {self.ip_address}"
