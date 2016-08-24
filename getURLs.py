
import os
import requests
import time

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from urllib.parse import urlparse



class GetUrls:

    def __init__(self, url, downloadDirectory, maxDepth):
        self.url = url
        self.downloadDirectory = os.path.abspath(downloadDirectory)
        self.maxDepth = maxDepth

    def getLinks(self):
        if not os.path.exists(self.downloadDirectory):
            os.makedirs(self.downloadDirectory)
        self.downloadUrlRespose(self.url, self.downloadDirectory, 0, self.maxDepth)

    def downloadUrlRespose(self, url, directory, depth, maxDepth):
        currentWorkingDirectory = os.getcwd()
        os.chdir(directory)
        r = requests.get(url)

        print("URL :" + url)

        if r.headers['Content-type'].split(';')[0].strip() == 'text/html':
            soup = BeautifulSoup(r.text, 'html.parser')
            with open('page.html', 'w') as file:
                file.write(str(soup.prettify(encoding='utf-8')))
                # fh.write(soup.prettify())
            if depth+1 > maxDepth:
                os.chdir(currentWorkingDirectory)
                return
            for index, link in enumerate(soup.find_all('a')):
                link_dir = os.path.abspath('link_'+str(index))
                os.mkdir(link_dir)
                href = link.get('href')
                if href:
                    if href.startswith('http://') or href.startswith('https://'):
                        self.downloadUrlRespose(href, link_dir, depth + 1, maxDepth)
                    elif href.startswith('/'):
                        parsedUrl = urlparse(url)
                        self.downloadUrlRespose(parsedUrl.scheme + '://' + parsedUrl.netloc + href, link_dir, depth + 1, maxDepth)
                    else:
                        print("here :" + href)
                        self.downloadUrlRespose(url.rstrip('/') + '/' + href, link_dir, depth + 1, maxDepth)


if __name__ == '__main__':
    argumentParser = ArgumentParser()
    argumentParser.add_argument('url', help='url to be downloaded')
    argumentParser.add_argument('-dir', help='download directory (defaults to current directory)', default=os.getcwd() + "\\" + str(int(time.time())), type=str)
    argumentParser.add_argument('-maxDepth', help='maximum depth of downloading links(defaults to 1)', default=1, type=int)
    args = argumentParser.parse_args()
    getUrls = GetUrls(args.url, args.dir, args.maxDepth)
    getUrls.getLinks()
