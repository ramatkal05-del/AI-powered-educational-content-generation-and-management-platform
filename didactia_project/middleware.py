"""
Middleware placeholder — database initialization is no longer done at request time.

Migrations must be run at deploy time:
    python manage.py migrate --noinput

Remove DatabaseInitializationMiddleware from MIDDLEWARE in settings.py.
This file is kept to avoid import errors during the transition.
"""
