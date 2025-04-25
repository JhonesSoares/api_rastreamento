from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Location

class Command(BaseCommand):
    help = 'Remove localizações com mais de 30 dias'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count, _ = Location.objects.filter(timestamp__lt=cutoff_date).delete()
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} localizações antigas removidas.'))
