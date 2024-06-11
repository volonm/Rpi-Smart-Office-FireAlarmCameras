# your_project/management/commands/runserver_custom.py

import threading
from django.core.management.commands.runserver import Command as RunServerCommand

def hello_world_thread():
    while True:
        print("Hello, World")

class Command(RunServerCommand):
    def inner_run(self, *args, **options):
        # Start the hello_world_thread when the server starts
        hello_thread = threading.Thread(target=hello_world_thread)
        hello_thread.daemon = True
        hello_thread.start()
        super().inner_run(*args, **options)
