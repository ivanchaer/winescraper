# This Python file uses the following encoding: utf-8

import codecs
import urllib2
import wine_urls
import time

import os
from os.path import join, getsize

class Scraper():

    scraped_html = ''

    downloaded_file_list = []

    not_yet_downloaded_list = []

    error_log_file = codecs.open('errors.txt', encoding="utf-8", mode="w")


    def __init__(self):

        self.init_scraping()


    def init_scraping(self):

        total = len(wine_urls.wine_urls)

        number_of_files_already_downloaded = len(self.already_downloaded()) 

        for wine_entry in self.not_yet_downloaded():
            wine_url = wine_entry[2]
            wine_id = wine_entry[1]

            

            output_file = codecs.open('pages/%s.html' % wine_id, encoding="utf-8", mode="w")

            percentage_complete = int(float(number_of_files_already_downloaded) / float(total) * 100)

            print >> output_file, self.retrieve_html(wine_url, wine_id).decode('utf-8')

            print 'File %s downloaded. %s percent complete' % (wine_id, percentage_complete)

            number_of_files_already_downloaded +=1

            time.sleep(4)


    def retrieve_html(self, wine_url, wine_id):

        try:
            xml = urllib2.urlopen(wine_url, timeout = 300).read()
            return xml

        except IOError:
            print >> self.error_log_file, 'IO Error found on id %s' % wine_id
            return ''
        else:
            print >> self.error_log_file, 'Error found on id %s' % wine_id
            return ''
    

    def already_downloaded(self):

        if len(self.downloaded_file_list) > 0:
            return self.downloaded_file_list

        for root, dirs, files in os.walk('pages'):
            downloaded_files = [page[0:-5] for page in files if getsize(join(root, page)) > 0]

        self.downloaded_file_list = downloaded_files

        return downloaded_files


    def not_yet_downloaded(self):

        if len(self.not_yet_downloaded_list) > 0:
            return self.not_yet_downloaded_list

        for wine_entry in wine_urls.wine_urls:
            wine_url = wine_entry[2]
            wine_id = wine_entry[1]

            if wine_id not in self.already_downloaded():
                self.not_yet_downloaded_list.append(wine_entry)

        return self.not_yet_downloaded_list

        




sc = Scraper()