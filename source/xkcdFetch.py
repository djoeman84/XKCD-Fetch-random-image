#!/usr/bin/env python
import re
import os
import sys
import urllib
import random
from mechanize import Browser
from bs4 import BeautifulSoup

"""

This program downloads a random image from xkcd to the directory from which the program was called from

This script is based on code by Jeremy Keeshin's scpd scraper (https://github.com/jkeesh).

In order for this to work you will need to download a few dependencies
1. BeautifulSoup for parsing: http://www.crummy.com/software/BeautifulSoup/
2. Mechanize for emulating a browser, http://wwwsearch.sourceforge.net/mechanize/

Usage: python /xkcdFetch.py "filePath" "fileName"


"""


def getRandomXKCDComic(urlBase):
    br = Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9')]
    br.set_handle_robots(False) 


    #XKCD Comics are enumerated in the following type by URL: http://www.xkcd.com/1, http://www.xkcd.com/2, ..., http://www.xkcd.com/n
    upperBound = 1
    lowerBound = 1

    #Multiply by two until address no longer exists
    while True:
        link = urlBase + str(upperBound) + "/"
        try:
            response = br.open(link)
        except:
            break

        lowerBound = upperBound
        upperBound = upperBound * 2

    #Binary Search for last Comic
    while True:
        pivot = (upperBound + lowerBound)/2
        link = urlBase + str(pivot) + "/"

        if lowerBound == upperBound or pivot == lowerBound:
            randomComicID = random.randint(1, pivot)
            randPageLink = urlBase + str(randomComicID) + "/"
            return br.open(randPageLink)
        try:
            response = br.open(link)
            lowerBound = pivot
        except:
            upperBound = pivot
    


def getRandomImageURL(urlBase):
    try:
        lastComic = getRandomXKCDComic(urlBase)
        soup = BeautifulSoup(lastComic.read())
        imageDIV = soup.find('div', attrs={'id': 'comic'})
        imgURL = imageDIV.img['src']
        return imgURL
    except Exception, e:
        raise e

def dowloadRandomImage(urlBase, filePath = "./", fileName = "xkcdComic.png"):
    if not os.path.isdir(filePath):
        malformedInput()
        return
    imgURL = getRandomImageURL(urlBase)
    uopen = urllib.urlopen(imgURL)
    stream = uopen.read()
    file = open(filePath + fileName, 'w')
    file.write(stream)
    file.close()
    print "Downloading " + imgURL


def malformedInput():
    print 'Malformed Input: Usage- ./xkcdFetch.py "filePath" "fileName"'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dowloadRandomImage("http://www.xkcd.com/")
    elif len(sys.argv) == 2:
        dowloadRandomImage("http://www.xkcd.com/", sys.argv[1])
    elif len(sys.argv) == 3:
        dowloadRandomImage("http://www.xkcd.com/", sys.argv[1], sys.argv[2])
    else:
        malformedInput()
    

