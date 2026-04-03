from django.core.management.base import BaseCommand
from didactia_project.initialization import setup_admin_user

class Command(BaseCommand):
    help = 'Create or update the superuser account from environment variables'

    def handle(self, *args, **options):
        self.stdout.write("Running ensure_admin...")
        try:
            setup_admin_user()
            self.stdout.write(self.style.SUCCESS("Successfully ran setup_admin_user"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error running setup_admin_user: {e}"))
