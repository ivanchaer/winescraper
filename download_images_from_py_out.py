# This Python file uses the following encoding: utf-8

import codecs

from lxml.html import parse
import urllib

import time

error_log_file = codecs.open('errors_saving_images.txt', encoding="utf-8", mode="w")

doc = parse('py-out.html').getroot()


def save_image(url,filename):
    if url != '':
        if url[0:2] == '//':
            url = 'http:' + url
        try:
            urllib.urlretrieve(url, filename)
            time.sleep(4)
        except IOError:
            print >> error_log_file, 'Error found on %s' % url
        
   
for wine in doc.cssselect('body > table > tr'):

    front_img = wine.cssselect('.front_bottle_img')[0].text.strip()
    back_img = wine.cssselect('.back_bottle_img')[0].text.strip()
    original_img = wine.cssselect('.original_img')[0].text.strip()
    wine_id = wine.cssselect('.wine_id')[0].text.strip()

    print original_img

    save_image(front_img, "images/%s_%s_%s.jpg" % (wine_id, 'front', '816x1544'))
    save_image(back_img, "images/%s_%s_%s.jpg" % (wine_id, 'back', '816x1544'))
    save_image(original_img, "images/%s_%s.jpg" % (wine_id, 'original'))
