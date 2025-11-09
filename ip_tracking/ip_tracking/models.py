# ip_tracking/models.py
from django.db import models


class RequestLog(models.Model):
    """Stores every incoming request with optional geolocation data."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.country}, {self.city} - {self.timestamp}"


class BlockedIP(models.Model):
    """List of blacklisted IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return f"Blocked: {self.ip_address}"


class SuspiciousIP(models.Model):
    """Stores IPs flagged by anomaly detection."""
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suspicious: {self.ip_address} - {self.reason}"
