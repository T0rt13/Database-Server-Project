import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, Error

load_dotenv() 
connectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']

def query1_createfile(connectionString, filePath, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    container = blob_service_client.get_container_client("databases_project")
    try:
        with open(file=os.path.join(filePath, fileName), mode="rb") as data:
            blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)
            if blob_client:
                return True
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def query3_getbloburl(connectionString, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    blob_client = blob_service_client.get_blob_client(container="databases_project", blob=fileName)
    try:
        with open(file=os.path.join(r'filepath', 'filename'), mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def query4_deleteblob(connectionString, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    try:
        blob_client = blob_service_client.get_blob_client(container="databases_project", blob=fileName)
        blob_client.delete_blob()
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def query5_editblob(connectionString, currentFileName, filePath, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    try:
        blob_client = blob_service_client.get_blob_client(container="databases_project", blob=currentFileName)
        blob_client.delete_blob()
        blob_client = blob_service_client.get_blob_client(container="databases_project", blob=fileName)
        with open(file=os.path.join(filePath, fileName), mode="rb") as data:
            container = blob_service_client.get_container_client("databases_project")
            blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)
    except Error as e:
        print(f"Error executing query: {e}")
        return None
