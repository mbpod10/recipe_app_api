from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """subclasses of BaseCommand must provide a handle() method"""

    def handle(self, *args, **options):
        # self.stdout.write(self.style.SUCCESS(
        # 'Successfully printed command!'))
        self.stdout.write(self.style.SUCCESS(args))
