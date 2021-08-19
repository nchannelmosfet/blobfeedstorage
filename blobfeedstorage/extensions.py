from scrapy.extensions.feedexport import BlockingFeedStorage
from azure.storage.blob import ContainerClient
from urllib.parse import urlparse

def parse_blob_uri(uri):
    path = urlparse(uri).path[1:] # remove leading /
    container_name, blob_name = path.split('/', 1) # first component is container, rest is file
    if container_name and not container_name.islower():
        raise ValueError(f'Container name {container_name} is not valid, must be lower-case. ')
    return container_name, blob_name


class BlobFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, conn_str=None, overwrite=False):
        self.overwrite = overwrite
        self.container_name, self.blob_name = parse_blob_uri(uri)
        
        self.container_client = ContainerClient.from_connection_string(conn_str, self.container_name)
        if not self.container_client.exists():
            self.container_client.create_container()

    @classmethod
    def from_crawler(cls, crawler, uri):
        return cls(
            uri,
            conn_str=crawler.settings['AZURE_STORAGE_CONN_STR'],
            overwrite=crawler.settings.getbool('AZURE_STORAGE_OVERWRITE')
        )

    def _store_in_thread(self, file):
        file.seek(0)
        
        self.container_client.upload_blob(self.blob_name, file, overwrite=self.overwrite)
        file.close()

