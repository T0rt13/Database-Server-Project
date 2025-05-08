import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv() 
connectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']

def query1_createfile(filePath, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    container = blob_service_client.get_container_client("databasesproject")
    with open(file=os.path.join(filePath, fileName), mode="rb") as data:
        blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)
        if blob_client:
            return True

def query3_getbloburl(fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    blob_client = blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
    with open(file=os.path.join(r'', fileName), mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())

def query4_deleteblob(fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    blob_client = blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
    blob_client.delete_blob()

def query5_editblob(currentFileName, filePath, fileName):
    blob_service_client = BlobServiceClient.from_connection_string(connectionString)
    blob_client = blob_service_client.get_blob_client(container="databasesproject", blob=currentFileName)
    blob_client.delete_blob()
    blob_client = blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
    with open(file=os.path.join(filePath, fileName), mode="rb") as data:
        container = blob_service_client.get_container_client("databasesproject")
        blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)

if __name__ == "__main__":
    filePath = ""
    fileName = "testfile.txt"
    newFileName = "testfile2.txt"
    query3_getbloburl(newFileName)

