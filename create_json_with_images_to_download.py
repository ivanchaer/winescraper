# This Python file uses the following encoding: utf-8

import codecs

from lxml.html import parse
import urllib

import time

from entries import wine_urls

import os
from os.path import join, getsize

class image_downloader():

    images_to_download = {}

    logs_root = './logs/download_images/'
    imgs_root = './images/'



    def __init__(self):

        self.error_log_file = codecs.open(self.logs_root + 'errors_saving_images.txt', encoding="utf-8", mode="w")
        self.image_urls_log_file = codecs.open('./logs/image_urls/image_urls.txt', encoding="utf-8", mode="r")


        for wine_id, images in self.files_to_download().iteritems():

            for image_type, image_url in images.iteritems():

                self.save_image(image_url, self.image_file_name(wine_id, image_type))


    def log(self, msg):
        print msg


    def image_file_name(self, wine_id, image_type):
        return '%s%s_%s.jpg' % (self.imgs_root, wine_id, image_type)


    def get_id_from_page_url(self, url):
        url = [wine_url[1] for wine_url in wine_urls if wine_url[2] == url][0:1][0] or []
        return url

    def files_to_download(self):

        if len(self.images_to_download) > 0:
            return self.images_to_download


        downloaded_images = []

        for root, dirs, files in os.walk('images'):
            downloaded_images = [image for image in files if getsize(join(root, image)) > 0 and image[-4:] == 'jpg']


        image_url_raw_list = self.image_urls_log_file.read().splitlines()


        wine_id = ''
        image_type = ''

        for line in image_url_raw_list:

            self.log(line)

            if line.startswith('// '):
                url = line.lstrip('// [\'').rstrip('\']')
                wine_id = self.get_id_from_page_url(url)
                self.log('WINE ID: -%s-' % url)
                self.images_to_download[wine_id] = {}

            else:


                if '204x400' in line:
                    image_type = 'original'
                elif '01_816x1544' in line:
                    image_type = 'front'
                elif '02_816x1544' in line:
                    image_type = 'back'
                elif line.startswith('//cache'):
                    image_type = 'label'

                if self.image_file_name(wine_id, image_type) not in downloaded_images:
                    self.images_to_download[wine_id][image_type] = line


        self.log(self.images_to_download)

        return self.images_to_download


    def save_image(self, url,filename):
        if url != '':
            if url[0:2] == '//':
                url = 'http:' + url
            try:

                urllib.urlretrieve(url, filename)

                self.log('saved %s to %s' % (url, filename))
                
                time.sleep(4)

            except IOError:
                print >> error_log_file, 'Error found on %s' % url


imgd = image_downloader()