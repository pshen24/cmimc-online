from django.core.management.base import BaseCommand
from website.tasks import init_all_tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        init_all_tasks()

