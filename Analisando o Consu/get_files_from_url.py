import urllib
from sgmllib import SGMLParser
import os


class URLLister(SGMLParser):
    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose=0)
        self.urls = []

    def reset(self):
        SGMLParser.reset(self)

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)


def get_pdf_links(url):
    print url
    # get urls from url
    try:
        usock = urllib.urlopen(url)
    except:
        print "Webpage not opened"
        if not os.path.exists("NotDownloaded"):
            os.makedirs("NotDownloaded")
        with open("NotDownloaded/links.txt", 'a') as f:
            f.write(url)
        return []
    parser = URLLister()
    parser.feed(usock.read())
    usock.close()
    parser.close()

    # filter urls
    pdf = []
    for url in parser.urls:
        if ".pdf" in url:  # if you change this for .txt for instance, you can get different typesfiles
            pdf.append(url)
    # print the number of files
    print len(pdf)
    return pdf


def download_pdf(url):
    # get the name o the original file (usually the name is the last part of the url
    rest, name = url.rsplit('/', 1)
    path = 'DownloadedFiles/' + name
    print name

    # download content
    try:
        urllib.URLopener().retrieve(url, path)
    except: # create a .csv of the not downloaded files
        print "Could not be downloaded"

        with open("NotDownloaded_links.csv", 'a') as f:
            f.write(url + '\n')


def main():
    # The url that you want to get the pdfs from
    rooturl = "http://www.sg.unicamp.br/consu/pautas-e-atas/ano-2000"

    pdfs = get_pdf_links(rooturl)

    if not os.path.exists('DownloadedFiles/'):
        os.makedirs('DownloadedFiles/')

    # download the content of a url (pdf in this case)
    for pdf_url in pdfs:
        download_pdf(pdf_url)


if __name__ == "__main__":
    main()
