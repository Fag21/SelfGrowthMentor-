from django.core.management.base import BaseCommand
from social_control.models import SocialAccount

class Command(BaseCommand):
    help = "Reset daily social media usage for all users"

    def handle(self, *args, **options):
        SocialAccount.objects.all().update(time_spent_today=0)
        self.stdout.write(self.style.SUCCESS("✅ Daily usage reset done"))
