#XKCD Fetch Random Comic

This program downloads a random image from xkcd to the directory from which the program was called from

This script is based on code by Jeremy Keeshin's scpd scraper (https://github.com/jkeesh).

In order for this to work you will need to download a few dependencies

1. BeautifulSoup for parsing: http://www.crummy.com/software/BeautifulSoup/
2. Mechanize for emulating a browser, http://wwwsearch.sourceforge.net/mechanize/

Usage: python /xkcdFetch.py "filePath" "fileName"