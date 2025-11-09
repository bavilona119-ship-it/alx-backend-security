# ip_tracking/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from ip_tracking.models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    """
    Celery task to detect suspicious IP activity.
    Runs hourly via Celery Beat.
    Flags IPs that:
      1. Exceed 100 requests/hour
      2. Access sensitive paths (/admin, /login)
    """
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # All recent requests (last 1 hour)
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # 1️⃣ High request volume: >100 per hour
    high_volume_ips = (
        recent_logs.values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in high_volume_ips:
        ip = entry['ip_address']
        reason = f"High request volume: {entry['request_count']} requests in the last hour"
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})

    # 2️⃣ Sensitive path access (/admin, /login)
    sensitive_paths = ['/admin', '/login']
    suspicious_by_path = recent_logs.filter(
        path__iregex='|'.join(sensitive_paths)
    ).values_list('ip_address', flat=True).distinct()

    for ip in suspicious_by_path:
        reason = "Accessed sensitive paths (/admin or /login)"
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})

    print(f"✅ Anomaly detection completed at {now.strftime('%Y-%m-%d %H:%M:%S')}")
