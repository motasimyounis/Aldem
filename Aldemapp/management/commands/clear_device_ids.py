from django.core.management.base import BaseCommand
from Aldemapp.models import Profile  # استبدل myapp باسم التطبيق الخاص بك

class Command(BaseCommand):
    help = 'Clear device_id field from all Profile objects'

    def handle(self, *args, **kwargs):
        Profile.objects.update(device_id=None)
        self.stdout.write(self.style.SUCCESS('Successfully cleared device_id from all profiles!'))
