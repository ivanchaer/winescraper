# This Python file uses the following encoding: utf-8

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import sys
import codecs
import time

from string import Template 

from wine_urls import wine_urls

class WebPage(QWebPage):
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"


class Browser(QWebView):

    # To be emitted when every items are downloaded
    done = Signal()

    url_idx = 0

    def __init__(self):


        super(Browser, self).__init__()

        st=self.settings()
        st.setAttribute(st.AutoLoadImages,False)

        self.outputFile = codecs.open('./py-out.html', encoding="utf-8", mode="w")
       
        self.loadFinished.connect(self.trigger_checks)

        self.formatted_data = ''


        print >> self.outputFile, '<table>'
        
        self.start()


    def current_url(self):
        return wine_urls[self.url_idx][2]
    
    def last_url(self):
        return self.url_idx == len(wine_urls)

    def start(self):
        self.page().mainFrame().load(self.current_url())


    def trigger_checks(self, ok):
        if ok:

            self.retrieve_data()

        else:
            print "Error while downloading %s\nSkipping."%self.currentUrl()
    
    def get_next(self):

        self.url_idx += 1

        self.page().mainFrame().load(self.current_url())


    def row_template(self, data):

        template = """
        <tr>
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
            <td class="bottle_img">
                $f_bottle_img
            </td>
            <td class="abv">
                $f_abv
            </td>
        </tr>
        """

        return Template(template).safe_substitute(data) 


    def retrieve_data(self):

        

        frame = self.page().mainFrame()
        doc = frame.documentElement()

        form = doc.findFirst("main")

        if not form.isNull():

            row_values = dict(
                f_url = self.current_url(),
                f_reviews = form.evaluateJavaScript(" $(this).find('ul.tabContents li.reviews').html() ").strip(),
                f_wine_maker_notes = form.evaluateJavaScript(" $(this).find('ul.tabContents li.aboutTheWine').html() ").strip(),
                f_the_winery = form.evaluateJavaScript(" $(this).find('ul.tabContents li.theWinery').html() ").strip(),
                f_bottle_img = form.evaluateJavaScript(" $(this).find('img.hero').attr('src')").strip(),
                f_abv = form.evaluateJavaScript(" $(this).find('li.abv').html() ").strip()
                
            )

            # self.formatted_data += self.row_template(row_values)

            print >> self.outputFile, self.row_template(row_values)



            if self.url_idx >= 4:
                print >> self.outputFile, '</table>'
             
                self.loadFinished.disconnect(self.retrieve_data)                        
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