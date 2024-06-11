import time
import subprocess
from threading import Thread

from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the Django development server with the scheduler.'

    def do_thread_work(self):
        i = 0
        while i <= 10:
            print("something")
            i = i + 1
            time.sleep(1)

    def goAndCheckVidoes(self):
        call_command("sync_videos_until_alert_stops")

    def handle(self, *args, **options):
        thread2 = Thread(target=self.goAndCheckVidoes)
        thread2.start()

        # Start the Django development server as a subprocess
        server_process = subprocess.Popen(['python', 'manage.py', 'runserver'])

        #thread2.join()  # Wait for the custom thread to finish
        #server_process.terminate()  # Terminate the server process
