from django.core.management.base import BaseCommand
import pyodbc
from sensors.models import SensorData, Raspberry, Recording, SystemStatus, SystemAlertLog
from datetime import datetime
import re
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from colorama import init, Fore
init(autoreset=True)

def syncOnlyModels():
    try:

        # Construct the path to cloudCredentials.txt
        config_file = os.path.join('sync_app', 'cloudCredentials.txt')

        # Initialize variables
        server = None
        database = None
        user = None
        password = None
        driver = None

        try:
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'server':
                            server = value
                        elif key == 'database':
                            database = value
                        elif key == 'user':
                            user = value
                        elif key == 'password':
                            password = value
                        elif key == 'driver':
                            driver = value

            print(Fore.GREEN + "==== TRYING TO SYNC THE MODELS ====")

            print(f"Server: {server}")
            print(f"Database: {database}")
            print(f"User: {user}")
            print(f"Password: {password}")
            print(f"Driver: {driver}")
        except FileNotFoundError:
            print("Config file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Define Azure database connection settings
        azure_db_settings = {
            'server': server,
            'database': database,
            'user': user,
            'password': password,
            'driver': driver,
        }

        # Create an Azure database connection
        azure_conn = pyodbc.connect(
            f"DRIVER={{{azure_db_settings['driver']}}};"
            f"SERVER={{{azure_db_settings['server']}}};"
            f"DATABASE={{{azure_db_settings['database']}}};"
            f"UID={{{azure_db_settings['user']}}};"
            f"PWD={{{azure_db_settings['password']}}};"
        )

        azure_cursor = azure_conn.cursor()

        ##### Retrieve data from the Raspberry model
        local_data = Raspberry.objects.all()
        print("Processing data for the Raspberry model")
        for item in local_data:
            # Check if a record with the same date and time exists in the Azure database
            azure_cursor.execute(
                "SELECT COUNT(*) FROM Raspberry WHERE name = ?",
                [item.name]
            )
            record_count = azure_cursor.fetchone()[0]

            if record_count == 0:
                # No matching record found, insert a new record
                azure_cursor.execute(
                    "INSERT INTO Raspberry (name, token) "
                    "VALUES (?, ?)",
                    [item.name, item.token]
                )
            else:
                # Matching record found, update the existing record
                azure_cursor.execute(
                    "UPDATE Raspberry SET name = ?, token = ? "
                    "WHERE name = ?",
                    [item.name, item.token, item.name]
                )

        ##### Retrieve data from the SensorData model
        local_data = SensorData.objects.all()
        print("Processing data for the SensorData model")
        for item in local_data:
            #print(item.date)
            # Check if a record with the same date and time exists in the database
            azure_cursor.execute(
                "SELECT COUNT(*) FROM SensorData WHERE date = ? AND time = ?",
                [item.date, item.time]
            )
            record_count = azure_cursor.fetchone()[0]

            if record_count == 0:
                # No matching record found, insert a new record
                azure_cursor.execute(
                    "INSERT INTO SensorData (rid_id, TEMP, CO, H2, CH4, LPG, PROPANE, ALCOHOL, SMOKE, date, time) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [item.rid_id, item.TEMP, item.CO, item.H2, item.CH4, item.LPG, item.PROPANE, item.ALCOHOL,
                     item.SMOKE, item.date, item.time]
                )
            else:
                # Matching record found, update the existing record
                azure_cursor.execute(
                    "UPDATE SensorData SET TEMP = ?, CO = ?, H2 = ?, CH4 = ?, LPG = ?, PROPANE = ?, ALCOHOL = ?, SMOKE = ? "
                    "WHERE date = ? AND time = ?",
                    [item.TEMP, item.CO, item.H2, item.CH4, item.LPG, item.PROPANE, item.ALCOHOL, item.SMOKE, item.date,
                     item.time]
                )

        #### Retrieve data from the Recording modal
        local_data = Recording.objects.all()
        print("Processing data for the Recording model")
        for item in local_data:
            #print(item.date)
            # Check if a record with the same date and time exists in the database
            azure_cursor.execute(
                "SELECT COUNT(*) FROM Recording WHERE date = ? AND time = ?",
                [item.date, item.time]
            )
            record_count = azure_cursor.fetchone()[0]

            if record_count == 0:
                # No matching record found, insert a new record
                azure_cursor.execute(
                    "INSERT INTO Recording (rid_id, date, time, [file]) "  # Enclose 'file' in square brackets
                    "VALUES (?, ?, ?, ?)",
                    [item.rid_id, item.date, item.time, item.file.path]
                )
            else:
                # Matching record found, update the existing record
                azure_cursor.execute(
                    "UPDATE Recording SET rid_id = ?, date = ?, time = ?, [file] = ? "  # Enclose 'file' in square brackets
                    "WHERE date = ? AND time = ?",
                    [item.rid_id, item.date, item.time, item.file.path, item.date, item.time]
                )

        # Commit the changes and close the Azure database connection
        # azure_cursor.commit()
        # azure_cursor.close()

        #### Retrieve data from the SystemAlertLog model
        local_data = SystemAlertLog.objects.all()
        print("Processing data for the SystemAlertLog model")
        for item in local_data:
            # Check if a record with the same date and time exists in the Azure database
            azure_cursor.execute(
                "SELECT COUNT(*) FROM SystemAlertLog WHERE date = ? AND time = ?",
                [item.date, item.time]
            )
            record_count = azure_cursor.fetchone()[0]

            if record_count == 0:
                # No matching record found, insert a new record
                azure_cursor.execute(
                    "INSERT INTO SystemAlertLog (rid_id, date, time, msg) "
                    "VALUES (?, ?, ?, ?)",
                    [item.rid, item.date, item.time, item.msg]
                )
            else:
                # Matching record found, update the existing record
                azure_cursor.execute(
                    "UPDATE SystemAlertLog SET rid_id = ?, date = ?, time = ?, msg = ? "
                    "WHERE date = ? AND time = ?",
                    [item.rid, item.date, item.time, item.msg, item.date, item.time]
                )

        #### Open and read the log file line by line
        with open('logs.txt', 'r') as file:
            lines = file.readlines()


        # Loop through the lines and insert them into the database
        print("Processing data for the logs")
        for line in lines:
            # Check if the log entry already exists in the database
            exists_query = f"SELECT COUNT(*) FROM logs WHERE log_entry = ?"
            azure_cursor.execute(exists_query, line.strip())
            count = azure_cursor.fetchone()[0]

            # If the log entry does not exist, insert it into the database
            if count == 0:
                # Replace 'column_name' with the name of the column in your table
                insert_query = f"INSERT INTO logs (log_entry) VALUES (?)"
                azure_cursor.execute(insert_query, line.strip())

        azure_cursor.commit()
        azure_cursor.close()
        azure_conn.close()

        print(Fore.GREEN + 'Models synchronization completed successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')


def syncVideos():
    try:

        # Initialize variables
        received_connection_string = None
        received_container_name = None

        config_file = os.path.join('sync_app', 'cloudCredentials.txt')

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
            print(Fore.GREEN + "==== TRYING TO SYNC THE VIDEOS ====")
            print(f"Connection String: {received_connection_string}")
            print(f"Container Name: {received_container_name}")
        except FileNotFoundError:
            print("Config file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        connection_string = received_connection_string
        container_name = received_container_name
        local_videos_directory = "media/documents"  # Adjust this path accordingly

        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get or create the container
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        # List existing blobs in the container
        existing_blobs = [blob.name for blob in container_client.list_blobs()]

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

        if __name__ == "__main__":
            upload_videos_to_azure_blob()


        print(Fore.GREEN + 'Video synchronization completed successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')