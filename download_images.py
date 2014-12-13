# This Python file uses the following encoding: utf-8

import codecs

from lxml.html import parse
import urllib

import time

from entries import wine_urls

import os
from os.path import join, getsize

import ast

class image_downloader():

    images_to_download = {}
    downloaded_images = []

    logs_root = './logs/download_images/'
    imgs_root = 'images/'



    def __init__(self):

        self.error_log_file = codecs.open(self.logs_root + 'errors_saving_images.txt', encoding="utf-8", mode="w")

    
        with open('./logs/download_images/images_to_download.txt') as data_file:
            print '###'
            print data_file 
            self.image_url_dict = ast.literal_eval(data_file.read())



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



        for root, dirs, files in os.walk('images'):
            self.downloaded_images = [join(root, image) for image in files if getsize(join(root, image)) > 0 and image[-3:] == 'jpg']


        return self.image_url_dict


    def save_image(self, url,filename):
        if url != '':

            if filename not in self.downloaded_images:


                if url[0:2] == '//':
                    url = 'http:' + url
                try:

                    urllib.urlretrieve(url, filename)

                    self.log('saved %s to %s' % (url, filename))
                    
                    time.sleep(1)

                except IOError:
                    print >> error_log_file, 'Error found on %s' % url

            else:
                self.log('ignoring url %s' % url)


imgd = image_downloader()