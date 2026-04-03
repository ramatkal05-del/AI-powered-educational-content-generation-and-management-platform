"""
Initialization helpers — called at deploy/startup time, NOT from middleware.

Usage (Render build command or Dockerfile):
    python manage.py migrate --noinput
    python manage.py setup_site
    python manage.py ensure_admin

These functions are kept here for reference by management commands.
"""

import logging
from decouple import config

logger = logging.getLogger(__name__)


def setup_admin_user():
    """Create or update the superuser account from environment variables.

    Call this from a management command at deploy time, not from a web request.
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        admin_email = config('ADMIN_EMAIL', default='admin@didactia.com')
        admin_password = config('ADMIN_PASSWORD', default='')
        admin_username = config('ADMIN_USERNAME', default='admin')

        if not admin_password:
            logger.info("[INIT] No ADMIN_PASSWORD set — skipping admin user setup.")
            return

        logger.info("[INIT] Setting up admin user: %s", admin_email)

        user, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                'username': admin_username,
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
            }
        )

        user.set_password(admin_password)
        user.is_staff = True
        user.is_superuser = True
        user.username = admin_username
        user.save()

        status = 'created' if created else 'updated'
        logger.info("[INIT] Admin user %s successfully.", status)

    except Exception:
        logger.exception("[INIT] Error setting up admin user.")
