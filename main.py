from datetime import datetime

import sys
from BeautifulSoup import BeautifulSoup
import requests
from urlparse import urlparse
import argparse

GOOD_CODES = [302, 200, 301]


def log(msg, level="VERB"):
    if (VERBOSE and level == "VERB") or level != "VERB":
        print "{} - {}: {}".format(datetime.now().strftime('%X'), level, msg)


# Argument parsing
parser = argparse.ArgumentParser(description='Process a web-page for broken <a> links.')
parser.add_argument("url", help="url of webpage to scan", type=str)
parser.add_argument("-r", "--href", help="include all href links, including stylesheets", action="store_true")
parser.add_argument("-v", "--verbose", help="enable verbose logging", action="store_true")
args = parser.parse_args()
VERBOSE = args.verbose

headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}

# make sure requests can parse the url
if not args.url.startswith('http://') or args.url.startswith('https://'):
    args.url = 'http://' + args.url

log("Scanning URL: {}".format(args.url), "INFO")
r = requests.get(args.url, headers=headers, allow_redirects=True)

bs = BeautifulSoup(r.text)
elem = None
if not args.href:
    elem = bs.findAll('a')
else:
    elem = bs.findAll(href=True)

for i, a in enumerate(elem):
    try:
        url = a['href']
    except KeyError:
        log("Error getting url for element.")
        continue
    log("Retrieving headers for url: {}".format(url))
    if not url.startswith('#'):
        if not url.startswith('http'):
            parsed_uri = urlparse(args.url)
            url = '{uri.scheme}://{uri.netloc}/{url}'.format(url=url, uri=parsed_uri)
        try:
            req = requests.head(url, headers=headers, allow_redirects=True)
        except:
            pass
        else:
            log("Got status code {} for url {}".format(req.status_code, url))
            if req.status_code not in GOOD_CODES:
                log("{}, code: {}".format(a, req.status_code), "ERROR")
log("Done.", "INFO")
