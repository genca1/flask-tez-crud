import requests
import xml.etree.ElementTree as ET
from flask import jsonify

url = "http://www.tcmb.gov.tr/kurlar/today.xml"

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

xml = requests.get(url)
tree = ET.fromstring(xml.content)
arr = []
def findCurrency(name):
    for curr in tree.findall('Currency'):
        if name == 'Dolar':
            if curr.attrib['CurrencyCode'] == 'USD':
                buy = curr.find('ForexBuying').text
        elif name == 'Euro':
            if curr.attrib['CurrencyCode'] == 'EUR':
                buy = curr.find('ForexBuying').text
        elif name == 'Pound':
            if curr.attrib['CurrencyCode'] == 'GBP':
                buy = curr.find('ForexBuying').text
        elif name == 'Ruble':
            if curr.attrib['CurrencyCode'] == 'RUB':
                buy = curr.find('ForexBuying').text
    jarr = [
        { "Kur" : buy }
        ]
    return jsonify(results=jarr)
