# LinkDetector

A lightweight script to detect broken links on a page.

Scans all `<a/>` links with options to check all elements with `href` attributes.


```
usage: main.py [-h] [-r] [-v] url

Process a web-page for broken <a> links.

positional arguments:
  url            url of webpage to scan

optional arguments:
  -h, --help     show this help message and exit
  -r, --href     include all href links, including stylesheets
  -v, --verbose  enable verbose logging
```