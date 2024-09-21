from django.core.management.base import BaseCommand
from library.consumer import BackendConsumer


class Command(BaseCommand):
    help = 'Launches Listener for frontend events : RabitMQ'

    def handle(self, *args, **options):
        td = BackendConsumer()
        td.start()
        self.stdout.write("Started Consumer Thread")
