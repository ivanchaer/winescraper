from lxml import etree

import urllib

from StringIO import StringIO

import requests

url = 'http://www.wine.com/v6/Jordan-Cabernet-Sauvignon-2007/wine/110439/Detail.aspx'

xml = urllib.urlopen(url).read()

parser = etree.XMLParser(recover=True)


tree   = etree.parse(StringIO(xml), parser)

xml_obj = tree.xpath("//p[@id='ctl00_BodyContent_wineMakersNotesContent']")[0]

print(etree.tostring(xml_obj))

# img = tree.get_element_by_id('ctl00_BodyContent_wineMakersNotesContent')

