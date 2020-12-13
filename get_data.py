from urllib import request
import re
import requests


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


# Url with data
url = 'https://covid19.ssi.dk/overvagningsdata/download-fil-med-overvaagningdata'

# Open url as a byte array
fp = request.urlopen(url)
mybytes = fp.read()

# Decode into a string
mystr = mybytes.decode("utf8")
fp.close()

# Using regex to find all the relevant links
all_links = re.findall(r'<a href=\"(.*?)\" target=\"_blank\"', mystr)
data_url = all_links[0]  # The first link is the latest

# Save as zip file
download_url(data_url, 'data/data.zip')
