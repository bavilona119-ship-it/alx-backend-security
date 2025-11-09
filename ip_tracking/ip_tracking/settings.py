# settings.py

INSTALLED_APPS = [
    # Default Django apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'ratelimit',          # 👈 for rate limiting

    # Local apps
    'ip_tracking',        # 👈 your security app
]

# ---------------------------------------------------
# 🔒 Rate-limit configuration
# ---------------------------------------------------
RATELIMIT_ENABLE = True
RATELIMIT_VIEW = 'ip_tracking.views.custom_ratelimited'

# Optional caching backend for ratelimit counters
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ratelimit_cache'
    }
}

# ---------------------------------------------------
# Include the ip_tracking routes
# ---------------------------------------------------
from django.urls import include, path

ROOT_URLCONF = 'your_project_name.urls'  # replace with your project’s actual name

# Example of including ip_tracking URLs (ensure urls.py exists)
# In your_project_name/urls.py add:
# path('ip_tracking/', include('ip_tracking.urls')),
