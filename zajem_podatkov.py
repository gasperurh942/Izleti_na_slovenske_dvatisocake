import os
import re
import requests

def shrani_html_seznam(url):
    stran = requests.get(url)
    with open('html_seznam.txt', 'w') as izhod:
        izhod.write(stran.text)

re_id_gore = re.compile(
    r'<tr bgcolor="#\.\.\.\.\.\."><td><a href=\.pot.asp\?gorovjeid=(?P<id1>\d+)&id=(?P<id2>\d+)&potid=(?P<id3>\d+)'
    )

def naredi_seznam_idjev(datoteka):
    with open(datoteka) as dat:
        html = dat.read()
        seznam = []
        for gora in re_id_gore.finditer(html):
            print(gora)
            seznam.append(0)
    return seznam

# shrani_html_seznam(
#    'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&'
#    'goraime=&VisinaMIN=2000&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhod'
#    'isceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zaht'
#    'evnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceM'
#    'AXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0'
#    '&mojaDolzina=0'
#    )

naredi_seznam_idjev('html_seznam.txt')
