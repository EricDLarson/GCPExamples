#!/usr/bin/python

# Sample download of large blob file from Google Cloud Storage
# using (chunked) resumable downloads

import google.auth
import google.auth.transport.requests as tr_requests
from google.resumable_media.requests import ChunkedDownload
from google.oauth2 import service_account
import urllib3
import io

urllib3.disable_warnings()

keyfile = '<yourkeyfile.json>'
bucket = 'edl-west'
blob = '1G-test.bin'
outfile = '/tmp/output-test.bin'

credentials = service_account.Credentials.from_service_account_file(
    keyfile,
    scopes=['https://www.googleapis.com/auth/devstorage.read_only']
)

transport = tr_requests.AuthorizedSession(credentials)

url_template = (
    u'https://www.googleapis.com/download/storage/v1/b/'
    u'{bucket}/o/{blob_name}?alt=media')
media_url = url_template.format(
    bucket=bucket, blob_name=blob)

chunk_size = 50 * 1024 * 1024  # 50MB
stream = io.BytesIO()
download = ChunkedDownload(
    media_url, chunk_size, stream)

fd = open(outfile, 'wb')

while (not download.finished):
  response = download.consume_next_chunk(transport)
  print download.bytes_downloaded
  fd.write(response.content)
