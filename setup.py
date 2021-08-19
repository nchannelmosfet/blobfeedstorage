import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="blobfeedstorage",
    version="0.1.0",
    author="Jerry Wu",
    author_email="nchannelmosfet@gmail.com",
    description="Enables Scrapy to use Azure Blob Storage as storage backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nchannelmosfet/blobfeedstorage",
    packages=setuptools.find_packages(),
    install_requires=[
        'scrapy',
        'azure-storage-blob',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
