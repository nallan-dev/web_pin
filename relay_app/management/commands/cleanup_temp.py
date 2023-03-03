from django.contrib.admin.models import LogEntry
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = "cleanup sessions data and admin_log"

    def handle(self, *args, **options):
        Session.objects.all().delete()
        LogEntry.objects.all().delete()
        print("Cleanup - Success!")
