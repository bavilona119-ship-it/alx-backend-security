# ip_tracking/views.py
from django.http import JsonResponse
from ratelimit.decorators import ratelimit


def rate_limit_view(request):
    """
    Sensitive view protected by IP-based rate limiting.

    - Authenticated users → 10 requests / minute
    - Anonymous users → 5 requests / minute
    """

    # Choose rate dynamically
    rate = '10/m' if request.user.is_authenticated else '5/m'

    # Apply rate limit manually
    @ratelimit(key='ip', rate=rate, block=True)
    def inner(request):
        user_type = "authenticated" if request.user.is_authenticated else "anonymous"
        return JsonResponse({
            "message": f"Request allowed for {user_type} user",
            "status": "success"
        })

    return inner(request)


def custom_ratelimited(request, exception=None):
    """
    Custom response when the rate limit is exceeded.
    """
    return JsonResponse({
        "error": "Rate limit exceeded. Please wait before retrying.",
        "status": "429 Too Many Requests"
    }, status=429)
