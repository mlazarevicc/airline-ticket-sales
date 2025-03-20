from datetime import datetime, date, timedelta
"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    karte = []

    for karta in sve_karte.values():
       # if type(karta["datum_prodaje"]) == str:
       #     karta["datum_prodaje"] = datetime.strptime(karta["datum_prodaje"],'%Y-%m-%d %H:%M:%S')
        if type(karta["datum_prodaje"]) == datetime:
            if karta["datum_prodaje"].date() == dan:
                karte.append(karta)
        elif karta["datum_prodaje"] == dan:
            karte.append(karta)

    return karte

"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    karte = []

    for let in svi_konkretni_letovi:
        if svi_konkretni_letovi[let]["datum_i_vreme_polaska"].date() == dan:
            for karta in sve_karte:
                if sve_karte[karta]["sifra_konkretnog_leta"] == let :
                    karte.append(sve_karte[karta])

    return karte

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    karte = []

    for karta in sve_karte.values():
        if karta["prodavac"]:
            if type(karta["prodavac"]) == str:
                if type(karta["datum_prodaje"]) == datetime:
                    if karta["datum_prodaje"].date() == dan and karta["prodavac"] == prodavac:
                        karte.append(karta)
                if karta["datum_prodaje"] == dan and karta["prodavac"] == prodavac:
                    karte.append(karta)
            else:
                if type(karta["datum_prodaje"]) == datetime:
                    if karta["datum_prodaje"].date() == dan and karta["prodavac"]["korisnicko_ime"] == prodavac:
                        karte.append(karta)
                if karta["datum_prodaje"] == dan and karta["prodavac"]["korisnicko_ime"] == prodavac:
                    karte.append(karta)

    return karte

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date) -> tuple:
    broj = 0
    suma = 0

    for karta in sve_karte.values():
        if type(karta["datum_prodaje"]) == datetime:
            if karta["datum_prodaje"].date() == dan:
                suma += svi_letovi[svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
                broj += 1
        elif karta["datum_prodaje"] == dan:
                suma += svi_letovi[svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
                broj += 1
    
    return broj, suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date) -> tuple:
    broj = 0
    suma = 0

    if type(dan) == datetime:
        dan = dan.date()
        
    for let in svi_konkretni_letovi:
        if svi_konkretni_letovi[let]["datum_i_vreme_polaska"].date() == dan:
            for karta in sve_karte.values():
                if karta["sifra_konkretnog_leta"] == let:
                    broj += 1
                    suma += svi_letovi[svi_konkretni_letovi[let]["broj_leta"]]["cena"]

    return broj, suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, konkretni_letovi: dict, svi_letovi: dict,
                                                           dan: date, prodavac: str) -> tuple:
    broj = 0
    suma = 0

    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        if karta["prodavac"]:
            if type(karta["prodavac"]) == dict:
                if karta["datum_prodaje"].date() == dan and karta["prodavac"]["korisnicko_ime"] == prodavac:
                    broj += 1
                    suma += svi_letovi[konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
            else:
                if karta["datum_prodaje"].date() == dan and karta["prodavac"] == prodavac:
                    broj += 1
                    suma += svi_letovi[konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]

    return broj, suma

"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict) -> dict: #ubc znaci ukupan broj i cena
    prodaje = {}
    pocetni_datum = date.today() - timedelta(days=30)

    prodavci = []
    for karta in sve_karte.values():
        if karta["prodavac"]:
            if type(karta["prodavac"]) == str:
                prodavci.append(karta["prodavac"])
            else:
                prodavci.append(karta["prodavac"]["korisnicko_ime"])

    for prodavac in prodavci:
        podaci = [0, 0, prodavac]

        for karta in sve_karte.values():
            if karta["prodavac"]:
                if type(karta["prodavac"]) == str: 
                    prodavac2 =  karta["prodavac"]
                else: 
                    prodavac2 = karta["prodavac"]["korisnicko_ime"]
            
                if prodavac == prodavac2:
                    if type(karta["datum_prodaje"]) == datetime: 
                        datum = karta["datum_prodaje"].date()
                    elif type(karta["datum_prodaje"]) == str: 
                        datum = datetime.strptime(karta["datum_prodaje"],'%d.%m.%Y.').date()
                    else:
                        datum = karta["datum_prodaje"].date()

                    if datum > pocetni_datum:
                        podaci[0] += 1
                        podaci[1] += svi_letovi[svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
            
        prodaje[prodavac] = podaci

    return prodaje