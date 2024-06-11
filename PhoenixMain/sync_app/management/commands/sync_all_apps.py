from django.core.management.base import BaseCommand
import pyodbc
from sensors.models import SensorData, Raspberry, Recording, SystemStatus, SystemAlertLog
from datetime import datetime
import re
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from sync_app.management.commands.functions_for_sync import syncOnlyModels, syncVideos
from colorama import init, Fore
init(autoreset=True)


class Command(BaseCommand):
    help = 'Synchronize data from the local database to the Azure database for the SensorData model'

    def extract_timestamp(self, log_entry):
        # Define pattern
        timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'

        # Search for the timestamp in the log entry
        match = re.search(timestamp_pattern, log_entry)

        if match:
            timestamp_str = match.group(1)  # Extract the matched timestamp string
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')  # Parse the timestamp string
            return timestamp
        else:
            return None  # Return None if timestamp not found

    def log_entry_exists(self, azure_cursor, log_data, log_timestamp):
        # Check if a log entry with the same data and timestamp exists in the LogTable
        azure_cursor.execute(
            "SELECT COUNT(*) FROM LogTable WHERE log_data = ? AND log_timestamp = ?",
            (log_data, log_timestamp)
        )
        result = azure_cursor.fetchone()

        # Return True if a matching entry exists
        return result[0] > 0


    def handle(self, *args, **options):

        try:
            syncOnlyModels()
            syncVideos()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

            ##################### UPLOAD ALL THE VIDEOS AS BLOBS ##################

        #     connection_string = received_connection_string
        #     container_name = received_container_name
        #     local_videos_directory = "media/documents"  # Adjust this path accordingly
        #
        #     # Create a BlobServiceClient using the connection string
        #     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        #
        #     # Get or create the container
        #     container_client = blob_service_client.get_container_client(container_name)
        #     if not container_client.exists():
        #         container_client.create_container()
        #
        #     # List existing blobs in the container
        #     existing_blobs = [blob.name for blob in container_client.list_blobs()]
        #
        #     # List all video files in the local directory and upload if not already in the container
        #     for root, dirs, files in os.walk(local_videos_directory):
        #         for file in files:
        #             local_file_path = os.path.join(root, file)
        #             blob_name = os.path.relpath(local_file_path, local_videos_directory).replace("\\", "/")
        #
        #             # Check if the blob is already in the container
        #             if blob_name not in existing_blobs:
        #                 blob_client = container_client.get_blob_client(blob_name)
        #
        #                 with open(local_file_path, "rb") as data:
        #                     blob_client.upload_blob(data)
        #
        #     if __name__ == "__main__":
        #         upload_videos_to_azure_blob()
        #
        #
        #
        #     self.stdout.write(self.style.SUCCESS('Data synchronization completed successfully.'))
        # except Exception as e:
        #     self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

