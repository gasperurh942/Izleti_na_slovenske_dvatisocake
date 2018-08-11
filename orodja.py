def pretvori_zahtevnost(niz):
    zahtevnosti = []
    l = niz.split(',')
    for zaht in l:
        if 'zelo' in zaht:
            zahtevnosti.append(4)
        elif 'izjemno' in zaht:
            zahtevnosti.append(5)
        elif 'alpini' in zaht:
            zahtevnosti.append(6)
        elif 'delno' in zaht:
            zahtevnosti.append(2)
        elif 'lahk' in zaht:
            zahtevnosti.append(1)
        else:
            zahtevnosti.append(3)
    return max(zahtevnosti)

def pretvori_stevilo(zaht):
    if zaht == 6:
        return 'alpinistični vzpon'
    if zaht == 5:
        return 'izjemno zahtevna pot'
    if zaht == 4:
        return 'zelo zahtevna pot'
    if zaht == 3:
        return 'zahtevna pot'
    if zaht == 2:
        return 'delno zahtevna pot'
    if zaht == 1:
        return 'lahka pot'

def oznacenost(niz):
    if 'brezpotje' in niz:
        return 3
    elif 'neozn' in niz:
        return 2
    else:
        return 1

def pretvori_oznacenost(st):
    if st == 1:
        return 'označena pot'
    if st == 2:
        return 'neoznačena pot'
    if st == 3:
        return 'brezpotje'
