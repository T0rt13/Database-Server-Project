import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connectionString = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")