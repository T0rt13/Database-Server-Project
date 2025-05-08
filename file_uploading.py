import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv() 
connectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']

class BlobOperations:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(connectionString)

    def query1_createfile(self, filePath, fileName):
        container = self.blob_service_client.get_container_client("databasesproject")
        with open(file=os.path.join(filePath, fileName), mode="rb") as data:
            blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)
            if blob_client:
                return True

    def query3_getbloburl(self, fileName):
        blob_client = self.blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
        # with open(file=os.path.join(r'', fileName), mode="wb") as sample_blob:
        #     download_stream = blob_client.download_blob()
        #     sample_blob.write(download_stream.readall())
        download_stream = blob_client.download_blob()
        content = download_stream.readall()
        return content


    def query4_deleteblob(self, fileName):
        blob_client = self.blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
        blob_client.delete_blob()

    def query5_editblob(self, currentFileName, filePath, fileName):
        blob_client = self.blob_service_client.get_blob_client(container="databasesproject", blob=currentFileName)
        blob_client.delete_blob()
        blob_client = self.blob_service_client.get_blob_client(container="databasesproject", blob=fileName)
        with open(file=os.path.join(filePath, fileName), mode="rb") as data:
            container = self.blob_service_client.get_container_client("databasesproject")
            blob_client = container.upload_blob(name=fileName, data=data, overwrite=True)
