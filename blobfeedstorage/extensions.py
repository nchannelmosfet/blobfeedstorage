from scrapy.extensions.feedexport import BlockingFeedStorage
from azure.storage.blob import BlobServiceClient


def parse_blob_uri(uri):
    container_name = uri.split('/')[-2]
    if not container_name.islower():
        raise ValueError(f'Container name {container_name} is not valid, must be lower-case. ')
    blob_name = uri.split('/')[-1]
    return container_name, blob_name


class BlobFeedStorage(BlockingFeedStorage):

    def __init__(self, uri, conn_str=None):
        self.container_name, self.blob_name = parse_blob_uri(uri)
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    @classmethod
    def from_crawler(cls, crawler, uri):
        return cls(
            uri,
            conn_str=crawler.settings['AZURE_STORAGE_CONN_STR']
        )

    def _store_in_thread(self, file):
        file.seek(0)
        container_client = self.blob_service_client.get_container_client(self.container_name)
        if not container_client.exists():
            container_client.create_container()

        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=self.blob_name
        )
        blob_client.upload_blob(file)
        file.close()

