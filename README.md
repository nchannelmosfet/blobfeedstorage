# blobfeedstorage
This extension enables Scrapy to use Azure Blob Storage as storage backend.

# Installation
```
pip install git+https://github.com/nchannelmosfet/blobfeedstorage
```

# Example Usage
Add the following custom_settings to your scrapy spider. 
Credit: QuotesSpider from https://docs.scrapy.org/en/latest/intro/overview.html
```
from blobfeedstorage import BlobFeedStorage
from blobfeedstorage.utils import fullname
import scrapy
import os


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    custom_settings = {
        # Expect feed uri in the form of blob://<storage_accout_name>.blob.core.windows.net/<container_name>/<blob_name>
        # <blob_name> can root level or nested
        'FEEDS': {
            'blob://my-storage-account.blob.core.windows.net/blob-container/spiders/%(name)s_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
            }
        },
        # FEED_STORAGES defined here are merged with FEED_STORAGES_BASE
        'FEED_STORAGES': {
            'blob': fullname(BlobFeedStorage)  # fulname() gets fully qualified name of BlobFeedStorage
        },
        'AZURE_STORAGE_CONN_STR': os.getenv('AZURE_STORAGE_CONN_STR')   # authorize via connection string
        'AZURE_STORAGE_OVERWRITE': True     # allow existing blob to be overwritten, default False
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

```

# Disclaimer
I didn't see any official or 3rd party support for feed export to Azure Blob Storage.
So I decided to do it myself after reading the S3FeedStorage and GCSFeedStorage implementations at: 
https://github.com/scrapy/scrapy/blob/2.5/scrapy/extensions/feedexport.py. 
There are probably more ways that scrapy and Azure Blob Storage can interact with each other. 
But I am no expert in either, so I kept it as simple as possible. 
