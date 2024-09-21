from django.core.management.base import BaseCommand
# from library.consumer import FrontendListener
from library.consumer import FrontendListener


class Command(BaseCommand):
    help = 'Launches Listener for backend events : RabitMQ'

    def handle(self, *args, **options):
        td = FrontendListener()
        td.start()
        self.stdout.write("Started Consumer Thread")
