import os
import re
import requests

def shrani_html_seznam(url):
    stran = requests.get(url)
    with open('html_seznam.txt', 'w', encoding='utf-8') as izhod:
        izhod.write(stran.text)

re_id_izleta = re.compile(
    r'<tr bgcolor="#[ef5]{6}"><td><a href=\Wpot.asp.gorovje'
    r'id=(?P<id1>\d+)&id=(?P<id2>\d+)&potid=(?P<id3>\d+)\W>',flags=re.DOTALL
    )

re_podatki_izleta = re.compile(
    r'<meta\shttp-equiv="content-type"\scontent="text/html;\scharset=UTF-8" />'
    r'.*'
    #izhodišče
    r'<title>\s*(?P<izhodisce>[\s\w\(\)/\\.-]+)'
    r'€'
    #vrh
    r'(?P<vrh>[\s\w\(\)/\\.-]+)'
    #morebitna opomba glede smeri poti
    r'€'
    r'(?P<via>[,\s\w\(\)/\\.-]+)?</title>'
    r'.*'
    #gorovje
    r'<a\sclass="moder"\shref="/gorovja">gorovja</a>&nbsp;/&nbsp;<a\sclass="mod'
    r'er"\shref="/gorovje/[\w_]+/\d+">(?P<gorovje>[\w\s]+)</a>'
    r'.*'
    #višina izhodišča
    r'<tr><td><b>Izhodišče:</b>\s<?a?[\w\s_=/]*>?\s?[\w\s/\(\)-\\.]+\((?P<visina_izhodisca>\d+)'
    r'\sm\)<?/?a?>?</td></tr>'
    r'.*'
    #višina cilja
    r'<tr><td><b>Cilj:</b>\s<a\sclass="moder"\shref="/gora/[\w_-]+/\d+/\d+">'
    r'[^\n]+\((?P<visina>\d+)\sm\)</a></td></tr>'
    r'.*'
    #čas hoje
    r'<tr><td><b>Čas&nbsp;hoje:</b>\s(?P<cas_hoje>[\w&;]+)</td></tr>',
    flags=re.DOTALL
    )

def naredi_seznam_idjev(datoteka):
    with open(datoteka) as dat:
        html = dat.read()
        seznam = []
        for pot in re_id_izleta.finditer(html):
            seznam.append((pot.group(1), pot.group(2), pot.group(3)))
    return seznam

def shrani_strani_v_mapo(imenik):
    os.makedirs(imenik, exist_ok=True)
    for pot in naredi_seznam_idjev('html_seznam.txt'):
        url = 'http://www.hribi.net/pot.asp?gorovjeid={}&id={}&potid={}'.format(
            pot[0], pot[1], pot[2]
            )
        posamezna_pot = requests.get(url)
        ime_datoteke = 'pot-{}-{}-{}.html'.format(pot[0], pot[1], pot[2])
        polna_pot_datoteke = os.path.join(imenik, ime_datoteke)
        with open(polna_pot_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(posamezna_pot.text[:30000])

def izlusci_cas_hoje(niz):
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
    return ure * 60 + minute

def preberi_podatke_izletov(imenik):
    izleti = []
    for datoteka in os.listdir(imenik):
        polna_pot_datoteke = os.path.join(imenik, datoteka)
        with open(polna_pot_datoteke, encoding='utf-8') as vhod:
            niz = vhod.read().replace(' - ', '€',2)
            uspeh = re_podatki_izleta.search(niz)
            if uspeh:
                podatki = uspeh.groupdict()
                
                podatki['cas_hoje'] = izlusci_cas_hoje(podatki['cas_hoje'])
                
                izleti.append(podatki)
            else:
                print(polna_pot_datoteke)
                break
            

# shrani_html_seznam(
#    'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&'
#    'goraime=&VisinaMIN=2000&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhod'
#    'isceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zaht'
#    'evnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceM'
#    'AXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0'
#    '&mojaDolzina=0'
#    )

preberi_podatke_izletov('izleti')
