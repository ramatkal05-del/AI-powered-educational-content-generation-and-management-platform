"""
Signal handlers for the accounts app.
Loaded once via AccountsConfig.ready() in apps.py.
"""

import logging
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# UserProfile auto-creation
# ---------------------------------------------------------------------------

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensure every new user gets a UserProfile and an activity log entry."""
    if not created:
        return

    # Auto-create UserProfile
    try:
        from accounts.models import UserProfile
        UserProfile.objects.get_or_create(user=instance, defaults={'timezone': 'UTC'})
    except Exception:
        logger.exception("Failed to create UserProfile for user %s", instance.pk)

    # Log account creation activity
    try:
        from accounts.models import log_user_activity
        log_user_activity(
            user=instance,
            activity_type='account_created',
            description=f'Account created for {instance.get_full_name()}',
        )
    except Exception:
        logger.exception("Failed to log account creation activity for user %s", instance.pk)


# ---------------------------------------------------------------------------
# Login notification / logging
# ---------------------------------------------------------------------------

@receiver(user_logged_in)
def send_login_notification(sender, user, request, **kwargs):
    """Log user login for security auditing."""
    try:
        ip_address = _get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')[:100]
        logger.info(
            "User login: %s (%s) from %s at %s using %s",
            user.username, user.email, ip_address, timezone.now(), user_agent,
        )
    except Exception:
        logger.exception("Error in login notification handler.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_client_ip(request):
    """Return the client's real IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
