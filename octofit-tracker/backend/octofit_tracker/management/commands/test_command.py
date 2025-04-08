from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test Command for debugging Django management commands'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Test Command executed successfully.'))
