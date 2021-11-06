from io import BytesIO
import uuid
from typing import Union
from app.core.configuration import APP_STORAGE_CONNECTION_STRING, APP_STORAGE_CONTAINER
from azure.storage.blob import BlobServiceClient

connect_str = APP_STORAGE_CONNECTION_STRING
container_name = APP_STORAGE_CONTAINER


def upload(
    data: bytes, extension: str = ".png", metadata: dict = None, tags: dict = None
) -> Union[str, None]:
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    file_name = str(uuid.uuid4()) + extension

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )

    print("\nUploading to Azure Storage as blob:\n\t" + file_name)

    # Upload the created file
    try:
        d = blob_client.upload_blob(data)
        if metadata is not None:
            blob_client.set_blob_metadata(metadata)
        if tags is not None:
            blob_client.set_blob_tags(tags)
        return blob_client.url
    except Exception as e:
        print(e)
        return None