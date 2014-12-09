import codecs

import urllib

import re

import wine_urls

from string import Template 
import templates

class Scraper():

    scraped_html = ''

    output_file = codecs.open('./scraped.xml', encoding="utf-8", mode="w")

    def __init__(self):

        self.init_scraping()



    def init_scraping(self):

        print >> self.output_file, '<?xml version="1.0" encoding="UTF-8"?>'

        for wine_entry in wine_urls.wine_urls:
            wine_url = wine_entry[2]
            wine_id = wine_entry[1]

            self.retrieve_html(wine_url)

            wine_data = self.output_field_template(field_label='winemakers_notes', field_content=self.get_winemakers_notes()) + \
                self.output_field_template(field_label='critical_acclaim', field_content=self.get_critical_acclaim()) + \
                self.output_field_template(field_label='community_reviews', field_content=self.get_community_reviews())

            print >> self.output_file, self.output_wine_template(wine_id = wine_id, wine_url = wine_url, wine_data = wine_data)

    def output_wine_template(self, wine_id, wine_url, wine_data):

        return Template(templates.wine_template).safe_substitute({
            'wine_id': wine_id,
            'wine_url': wine_url,
            'wine_data': wine_data
        })


    def output_field_template(self, field_label, field_content):

        return Template(templates.row_template).safe_substitute({'field_label': field_label, 'field_content': field_content})


    def retrieve_html(self, wine_url):
        xml = urllib.urlopen(wine_url).read()

        self.scraped_html = xml


    def get_html_chunk(self, string, delimiter_start, delimiter_end):


        output_string = delimiter_start + string.split(delimiter_start)[1]
        output_string = output_string.split(delimiter_end)[0]

        return output_string



    def get_winemakers_notes(self):

        
        notes_start = '<section class="wineMakerNotes"'
        notes_end = '<section class="criticalAcclaim"'

        return self.get_html_chunk(self.scraped_html, notes_start, notes_end)


    def get_critical_acclaim(self):

        
        notes_start = '<section class="criticalAcclaim"'
        notes_end = '<li class="tabContent theWinery"'

        return self.get_html_chunk(self.scraped_html, notes_start, notes_end)



    def get_community_reviews(self):

        
        notes_start = '<div class="CustomerReviews"'
        notes_end = '<div id="BRRelatedProducts"'

        return self.get_html_chunk(self.scraped_html, notes_start, notes_end)





sc = Scraper()