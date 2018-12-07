import xml.etree.ElementTree as ET
import requests
from flask import jsonify

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"
xml = requests.get(url)
tree = ET.fromstring(xml.content)
arr = []
def findSehir(name):
    arr = []
    for sehir in tree.findall('sehirler'):
        if sehir.find("ili").text == name:
            minim = sehir.find('Min')
            maxim = sehir.find('Mak')
            durum = sehir.find('Durum').text
            d = {
                "\u0131": "ı",
                "\u0130": "İ",
                 "\u00c7": "Ç",
                "\u00e7":"ç",
                "\u011f":"ğ",
                "\u011e": "Ğ",
                "\u015f":"ş",
                "\u015e": "Ş"
            }
            replace_all(durum, d)
            arr.append(durum)
            arr.append(minim.text)
            arr.append(maxim.text)
            jarr = [
                {"Durum": arr[0],
                 "Min": arr[1],
                 "Max": arr[2]}
            ]
            return jsonify(results=jarr)
