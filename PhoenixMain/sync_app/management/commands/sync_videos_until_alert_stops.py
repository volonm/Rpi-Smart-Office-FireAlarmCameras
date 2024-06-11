import os
import time
from django.core.management.base import BaseCommand
from azure.storage.blob import BlobServiceClient, ContainerClient
from sensors.models import SystemStatus
from sync_app.management.commands.functions_for_sync import syncVideos, syncOnlyModels
from colorama import init, Fore
init(autoreset=True)


class Command(BaseCommand):
    help = 'Upload new and unique videos to Azure Blob Storage'

    def handle(self, *args, **options):




        # Construct the path to cloudCredentials.txt
        config_file = os.path.join('sync_app', 'cloudCredentials.txt')
        print("In SYNC ALL VIDOES")
        try:
            latest_status = SystemStatus.objects.latest('id')  # Assuming the model has an 'id' field or a timestamp field
            status_value = latest_status.status
        except SystemStatus.DoesNotExist:
            print("SystemStatus not found in the database.")

        # Initialize variables
        received_connection_string = None
        received_container_name = None

        try:
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'connection_string':
                            received_connection_string = value
                        elif key == 'container_name':
                            received_container_name = value

            # Now you have the values in the respective variables
            print("=== FROM SYNC ALL VIDEOS UNTIL ALERT STOPS ===")
            print(f"Connection String: {received_connection_string}")
            print(f"Container Name: {received_container_name}")
        except FileNotFoundError:
            print("Config file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        connection_string = received_connection_string
        container_name = received_container_name
        local_videos_directory = "media/documents"  # Adjust this path accordingly
        upload_interval = 1  # Set the interval (in seconds) for checking and uploading new videos

        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get or create the container
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        while True:
            if(SystemStatus.objects.latest('id').status == True):
                print(Fore.GREEN + "ALERT DETECTED - VIDEO SYNC LOOP HAS BEEN STARTED!")
                while SystemStatus.objects.latest('id').status == True:
                    # List existing blobs in the container
                    existing_blobs = {blob.name for blob in container_client.list_blobs()}

                    try:
                        latest_status = SystemStatus.objects.latest('id')
                        status_value = latest_status.status
                        #print(Fore.GREEN + f" FOR LOOP ==> System Status: {status_value}")

                    except SystemStatus.DoesNotExist:
                        print("SystemStatus not found in the database.")

                    # List all video files in the local directory and upload if not already in the container
                    for root, dirs, files in os.walk(local_videos_directory):
                        for file in files:
                            local_file_path = os.path.join(root, file)
                            blob_name = os.path.relpath(local_file_path, local_videos_directory).replace("\\", "/")

                            # Check if the blob is already in the container
                            if blob_name not in existing_blobs:
                                blob_client = container_client.get_blob_client(blob_name)

                                with open(local_file_path, "rb") as data:
                                    blob_client.upload_blob(data)
                                    existing_blobs.add(blob_name)
                    #syncVideos()

                print(Fore.GREEN + "ALERT HAS BEEN DISABLED - LOOP ENDED")
                print(Fore.GREEN + "PENULTIMATE SYNC (VIDEO + MODELS)")

                time.sleep(3)
                syncVideos()
                syncOnlyModels()

                print(Fore.GREEN + "FINAL SYNC - sleep two minutes before the SYNC")
                time.sleep(10) #MODIFY TO 120
                syncVideos()

                self.stdout.write(self.style.SUCCESS(Fore.GREEN + 'ALL DATA synchronization completed successfully.'))