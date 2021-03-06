# This Python file uses the following encoding: utf-8

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import sys
import codecs
import time

from string import Template 

from wine_urls import wine_urls

import os
from os.path import join, getsize


class WebPage(QWebPage):
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"


class Browser(QWebView):

    # To be emitted when every items are downloaded
    done = Signal()

    url_idx = 0

    downloaded_file_list = []

    def __init__(self):


        super(Browser, self).__init__()

        st=self.settings()
        st.setAttribute(st.AutoLoadImages,False)

        self.outputFile = codecs.open('./py-out.html', encoding="utf-8", mode="w")
       
        self.loadFinished.connect(self.trigger_checks)

        self.formatted_data = ''


        print >> self.outputFile, '<!DOCTYPE html><html><head><title></title></head><body><table>'
        
        self.start()


    def files_to_parse(self):

        if len(self.downloaded_file_list) > 0:
            return self.downloaded_file_list

        for root, dirs, files in os.walk('pages'):
            downloaded_files = [join(root, page) for page in files if getsize(join(root, page)) > 0 and page[-4:] == 'html']

        self.downloaded_file_list = downloaded_files

        return downloaded_files

    def get_url_from_file_name(self, filename):
        wine_id = filename.split('/')[1][0:-5]
        return [wine_url[2] for wine_url in wine_urls if wine_url[1] == wine_id][0]

    def current_url(self):
        return self.files_to_parse()[self.url_idx]
    
    def last_url(self):
        return self.url_idx == len(self.files_to_parse())

    def start(self):
        self.page().mainFrame().load(self.current_url())


    def trigger_checks(self, ok):
        if ok:

            print 'Parsing %s' % self.current_url()
            self.retrieve_data()

        else:
            print "Error while downloading %s\nSkipping."%self.current_url()
    
    def get_next(self):

        self.url_idx += 1

        self.page().mainFrame().load(self.current_url())


    def row_template(self, data):

        template = """
        <tr>
            <td class="wine_id">
                $f_wine_id
            </td>
            <td class="url">
                $f_url
            </td>
            <td class="reviews">
                $f_reviews
            </td>
            <td class="wine_maker_notes">
                $f_wine_maker_notes
            </td>
            <td class="the_winery">
                $f_the_winery
            </td>
            <td class="original_img">
                $f_img
            </td>
            <td class="front_bottle_img">
                $f_front_bottle_img
            </td>
            <td class="back_bottle_img">
                $f_back_bottle_img
            </td>
            <td class="abv">
                $f_abv
            </td>
        </tr>
        """

        return Template(template).safe_substitute(data) 


    def generate_bottle_image_urls(self, original_image_url, bottle_position):

        if (original_image_url is None) or (len(original_image_url) == 0):
            return ''

        front_image = original_image_url.replace('_s/pi/n/','').replace('_spin_spin2/main_variation_na_view_01_204x400.jpg','_pdp2/zoom_variation_na_view_01_816x1544.jpg')
        back_image = front_image.replace('01_816x1544.jpg','02_816x1544.jpg')

        if bottle_position == 'front':
            return front_image

        return back_image

    def retrieve_data(self):

        # embed jquery
        self.page().mainFrame().evaluateJavaScript(open('jquery.js').read())

        frame = self.page().mainFrame()
        doc = frame.documentElement()

        form = doc.findFirst("main")

        if not form.isNull():

            row_values = dict(
                f_wine_id = self.current_url().split('/')[1][0:-5],
                f_url = self.get_url_from_file_name(self.current_url()),
                f_reviews = form.evaluateJavaScript(" $(this).find('ul.tabContents li.reviews').html() ").strip(),
                f_wine_maker_notes = form.evaluateJavaScript(" $(this).find('ul.tabContents li.aboutTheWine').html() ").strip(),
                f_the_winery = form.evaluateJavaScript(" $(this).find('ul.tabContents li.theWinery').html() ").strip(),
                f_img = form.evaluateJavaScript(" $(this).find('img.hero').attr('src')").strip(),
                f_front_bottle_img = self.generate_bottle_image_urls(form.evaluateJavaScript(" $(this).find('img.hero:not([alt~=label])').attr('src')"), 'front'),
                f_back_bottle_img = self.generate_bottle_image_urls(form.evaluateJavaScript(" $(this).find('img.hero:not([alt~=label])').attr('src')"), 'back'),
                f_abv = form.evaluateJavaScript(" $(this).find('li.abv').html() ").strip()
                
            )

            # self.formatted_data += self.row_template(row_values)

            print >> self.outputFile, self.row_template(row_values)



            if self.url_idx >= 4:
                print >> self.outputFile, '</table></body></html>'
             
                self.loadFinished.disconnect(self.trigger_checks)                        
                self.done.emit()

            else:
                self.get_next()

        else:
            self.get_next()




app = QApplication(sys.argv)
br = Browser()
br.show()
br.done.connect(app.quit)
app.exec_()