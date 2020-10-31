from django.core.management.base import BaseCommand
from website.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser("admin@example.com", "changethispassword", full_name="Admin")

