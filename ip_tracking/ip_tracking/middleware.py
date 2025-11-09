# ip_tracking/middleware.py

from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import geolocate
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    """Middleware to log IPs with geolocation and block blacklisted IPs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Check cache first
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                data = geolocate(ip)
                country = data.get('country_name')
                city = data.get('city')
                geo_data = {'country': country, 'city': city}
                cache.set(ip, geo_data, timeout=60 * 60 * 24)  # Cache for 24 hours
            except Exception:
                geo_data = {'country': None, 'city': None}

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )

        response = self.get_response(request)
        return response
