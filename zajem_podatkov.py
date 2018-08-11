import os
import re
import requests

def shrani_html_seznam(url):
    stran = requests.get(url)
    with open('html_seznam.txt', 'w', encoding='utf-8') as izhod:
        izhod.write(stran.text)

id_izleta = re.compile(
    r'<tr bgcolor="#[ef5]{6}"><td><a href=\Wpot.asp.gorovje'
    r'id=(?P<id1>\d+)&id=(?P<id2>\d+)&potid=(?P<id3>\d+)\W>',flags=re.DOTALL
    )

id_gore = re.compile(
    r'<tr\sbgcolor="#eeeeee"><td\scolspan="2"><a\shref="(?P<url>[\w\\.\?=&]+)'
    r'.*',
    flags=re.DOTALL
    )

podatki_izleta = re.compile(
    #gorovje
    r'<a\sclass="moder"\shref="/gorovja">gorovja</a>&nbsp;/&nbsp;<a\sclass="mod'
    r'er"\shref="/gorovje/[\w_]+/\d+">(?P<gorovje>[\w\s]+)</a>'
    r'.*'
    #izhodišče
    r'<tr><td><b>Izhodišče:</b>\s(<a\sclass=moder.*>|)(?P<izhodišče>[\w\s_=/]*)>?\s?[\w\s/\(\)-\\.]+\((?P<višina_izhodišča>\d+)'
    r'\sm\)(</a>|)</td></tr>'
    r'.*'
    #cilj
    r'<tr><td><b>Cilj:</b>\s<a\sclass="moder"\shref="/gora/[\w_-]+/\d+/\d+">'
    r'(?P<cilj>[^\n]+)\s\((?P<višina_cilja>\d+)\sm\)</a></td></tr>'
    r'.*'
    #opomba poti
    r'<tr><td><b>Ime poti:</b>\s(?P<opomba_poti>[^\n]+)</td></tr>'
    r'.*'
    #čas hoje
    r'<tr><td><b>Čas&nbsp;hoje:</b>\s(?P<čas_hoje>[\w&;]+)</td></tr>'
    r'.*'
    #zahtevnost
    r'<tr><td><b>Zahtevnost:</b>\s(?P<zahtevnost>[\w\s,]+)</td></tr>'
    r'.*'
    #višinska razlika po poti
    r'<tr><td><b>Višinska\srazlika\spo\spoti:</b>\s'
    r'(?P<višinska_razlika_po_poti>\d+)\sm</td></tr>'
    r'.*'
    #število ogledov
    r'<tr><td><b>Ogledov:</b>\s(?P<število_ogledov>\d*)</td></tr>'
    r'.*'
    #ocena
    r'var\socena=(?P<ocena>\d\d?)'
    r'.*'
    #število glasov
    r'(<img\ssrc="/slike/zvezdaBela2.png"\sid="s\d\d?">)+\s'
    r'(?P<število_glasov>\d*)&nbsp;glasov',
    flags=re.DOTALL
    )

podatki_gore = re.compile(
    r'.*'
    #ime gore
    r'<title>(?P<gora>[-\w\s\\.\(\),\/]+)</title>'
    r'.*'
    #koordinate
    r'(?P<širina>46,\d+)°N&nbsp;/&nbsp;(?P<dolžina>\d+,\d+)°E</a>'
    r'.*'
    #vrsta cilja
    r'<tr><td><b>Vrsta:</b>\s(?P<vrsta_cilja>[\w,\s]*)</td></tr>',
    flags=re.DOTALL
    )

def naredi_seznam_idjev(datoteka):
    with open(datoteka) as dat:
        html = dat.read()
        seznam = []
        for pot in id_izleta.finditer(html):
            seznam.append((pot.group(1), pot.group(2), pot.group(3)))
    return seznam

def shrani_poti_v_mapo(imenik, seznam):
    os.makedirs(imenik, exist_ok=True)
    for pot in seznam:
        url = 'http://www.hribi.net/pot.asp?gorovjeid={}&id={}&potid={}'.format(
            pot[0], pot[1], pot[2]
            )
        posamezna_pot = requests.get(url)
        ime_datoteke = 'pot-{}-{}-{}.txt'.format(pot[0], pot[1], pot[2])
        polna_pot_datoteke = os.path.join(imenik, ime_datoteke)
        with open(polna_pot_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(posamezna_pot.text[:30000])
            
def shrani_gore_v_mapo(imenik, seznam):
    os.makedirs(imenik, exist_ok=True)
    for pot in seznam:
        url = 'http://www.hribi.net/gora.asp?gorovjeid={}&id={}'.format(
            pot[0], pot[1]
            )
        posamezna_gora = requests.get(url)
        ime_datoteke = 'gora-{}-{}.txt'.format(pot[0], pot[1])
        polna_pot_datoteke = os.path.join(imenik, ime_datoteke)
        with open(polna_pot_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(posamezna_gora.text[:30000])

def izlusci_cas_hoje(niz):
    ura = False
    if 'h' in niz:
        ura = True
    ure = 0
    minute = 0
    for znak in niz:
        try:
            if ura:
                ure = ure * 10 + int(znak)
            else:
                minute = minute * 10 + int(znak)
        except:
            if znak == 'h':
                ura = False
    return str(ure * 60 + minute)

def preberi_podatke_izletov(imenik):
    izleti = []
    for datoteka in os.listdir(imenik):
        polna_pot_datoteke = os.path.join(imenik, datoteka)
        with open(polna_pot_datoteke, encoding='utf-8') as vhod:
            niz = vhod.read()
            uspeh = podatki_izleta.search(niz)
            if uspeh:
                podatki = uspeh.groupdict()
                
                podatki['čas_hoje'] = izlusci_cas_hoje(podatki['čas_hoje'])
                if podatki['opomba_poti'] == '-':
                    podatki['opomba_poti'] = None
                
                izleti.append(podatki)
            else:
                print(polna_pot_datoteke)
    return izleti

def preberi_podatke_gora(imenik):
    gore = []
    for datoteka in os.listdir(imenik):
        polna_pot_datoteke = os.path.join(imenik, datoteka)
        with open(polna_pot_datoteke, encoding='utf-8') as vhod:
            niz = vhod.read()
            uspeh = podatki_gore.search(niz)
            if uspeh:
                podatki = uspeh.groupdict()
                gore.append(podatki)
            else:
                print(polna_pot_datoteke)
    return gore

##shrani_html_seznam(
##    'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&'
##    'goraime=&VisinaMIN=2000&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhod'
##    'isceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zaht'
##    'evnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceM'
##    'AXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0'
##    '&mojaDolzina=0'
##    )

##seznam = naredi_seznam_idjev('html_seznam.txt')
##shrani_poti_v_mapo('izleti', seznam)
##shrani_gore_v_mapo('gore', seznam)

izleti = preberi_podatke_izletov('izleti')
gore = preberi_podatke_gora('gore')

for izlet in izleti:
    uspeh = False
    for g in gore:
        if g['gora'] == izlet['cilj']:
            izlet['širina_cilja'] = g['širina']
            izlet['dolžina_cilja'] = g['dolžina']
            izlet['vrsta_cilja'] = g['vrsta_cilja']

import csv
with open('izleti.csv', 'w', newline='') as datoteka:
    polja = [
        'gorovje',
        'izhodišče',
        'višina_izhodišča',
        'cilj',
        'višina_cilja',
        'opomba_poti',
        'čas_hoje',
        'zahtevnost',
        'višinska_razlika_po_poti',
        'število_ogledov',
        'ocena',
        'število_glasov',
        'širina_cilja',
        'dolžina_cilja',
        'vrsta_cilja'
    ]
    pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
    pisalec.writeheader()
    for izlet in izleti:
        pisalec.writerow(izlet)
