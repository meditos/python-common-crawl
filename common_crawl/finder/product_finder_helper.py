from io import BytesIO
import requests
import gzip
import time


# Downloads full page
def download_page(record):
    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1
    # We'll get the file via HTTPS so we don't need to worry about S3 credentials
    # Getting the file on S3 is equivalent however - you can request a Range
    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    url = prefix + record['filename']

    response = None
    try_count = 3  # max try cnt
    while try_count > 0:
        try:
            response = get_response(url, offset, offset_end)
            try_count = 0
        except:
            if try_count <= 0:
                print("Failed to retrieve: " + url + "\n")  # done retrying
            else:
                try_count -= 1  # retry
                time.sleep(0.5)  # wait 1/2 second then retry

    return response


def get_response(url, offset, offset_end):
    # We can then use the Range header to ask for just this set of bytes
    resp = requests.get(url, headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
    # The page is stored compressed (gzip) to save space
    # We can extract it using the GZIP library
    raw_data = BytesIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)
    # What we have now is just the WARC response, formatted:
    data = f.read().decode("utf-8")
    response = ""
    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n', 2)
        except:
            pass
    # print(response)
    return response