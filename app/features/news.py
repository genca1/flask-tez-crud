import xml.etree.ElementTree as ET
import requests
from flask import jsonify


url = "http://feeds.bbci.co.uk/turkce/rss.xml"
xml = requests.get(url)
tree = ET.fromstring(xml.content)
title = []
desc = []
def getNews(number):
    for channel in tree.findall('channel'):
        for item in channel:
            for i in item:
                if i.tag == 'title':
                    title.append(i.text)
                elif i.tag == 'description':
                    desc.append(i.text)
    jarr = dict(zip(title[1:number],desc[0:number]))
    return jsonify(results=jarr)