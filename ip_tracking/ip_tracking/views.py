# ip_tracking/views.py

from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# Rate limit decorator:
# - Authenticated: 10 requests/minute
# - Anonymous: 5 requests/minute

@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def sensitive_view(request):
    """Example sensitive view protected by rate limiting."""
    if request.user.is_authenticated:
        return JsonResponse({"message": "Authenticated user - allowed"})
    else:
        return JsonResponse({"message": "Anonymous user - allowed"})
