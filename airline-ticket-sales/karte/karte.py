from common import konstante
from functools import reduce
from datetime import datetime, date
import csv

sledeci_broj_karte = 0

def sledeci_broj_karte2(sve_karte: dict) -> int:
    broj = 0
    for broj2 in sve_karte:
        if broj2 > broj:
            broj = broj2
    return broj

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(sve_karte: dict, svi_konkretni_letovi: dict, sifra_konkretnog_leta: int, putnici: list, 
                   slobodna_mesta: list, kupac: dict, **kwargs): # -> (dict,dict)

    if not sifra_konkretnog_leta in svi_konkretni_letovi:
        raise Exception ("Prosleđeni let ne postoji.")

    if all(all(sediste) for sediste in slobodna_mesta):
        raise Exception ("Nema slobodnih mesta za ovaj let.")

    if kupac["uloga"] in (konstante.ULOGA_ADMIN,konstante.ULOGA_PRODAVAC):
        raise Exception ("Samo korisnici mogu kupiti kartu.")

    broj_karte = sledeci_broj_karte2(sve_karte)

    karta = {
        "broj_karte": broj_karte,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": konstante.STATUS_NEREALIZOVANA_KARTA,
        "obrisana": False,
        "kupac": kupac,
        "prodavac": "",
        "datum_prodaje": ""
    }

    if kwargs:
        for kljuc, podatak in kwargs.items():
            if kljuc == konstante.ULOGA_PRODAVAC and podatak["uloga"] != konstante.ULOGA_PRODAVAC:
                raise Exception ("Prodavac mora da proda kartu.")
            karta[kljuc] = podatak
    
    sve_karte[karta["broj_karte"]] = karta
    return (karta, sve_karte)

def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):
    nerealizovane_karte = []
    for karta in sve_karte:
        if korisnik in karta["putnici"] and karta["status"] == konstante.STATUS_NEREALIZOVANA_KARTA:
                nerealizovane_karte.append(karta)

    return nerealizovane_karte

"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(sve_karte: iter, svi_konkretni_letovi: iter, broj_karte: int, nova_sifra_konkretnog_leta: int=None,
                 nov_datum_polaska: datetime=None, sediste=None) -> dict:
    
    if broj_karte not in sve_karte:
        raise Exception ("Broj karte nije validan.")
    if nov_datum_polaska:
        svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"] = nov_datum_polaska
    if nova_sifra_konkretnog_leta:
        #if nova_sifra_konkretnog_leta in svi_konkretni_letovi:
        #    raise Exception ("Konkretni let sa tom sifrom vec postoji.")
        sve_karte[broj_karte]["sifra_konkretnog_leta"] = nova_sifra_konkretnog_leta

    if 'zauzetost' in svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]].keys():
        matrica = svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]["zauzetost"]
        kolona, red = ord(sediste[2:]) - 1, ord(sediste[:2]) - 65

        if matrica[red][kolona]:
            raise Exception ("Sediste je zauzeto.")
        sve_karte[broj_karte]["sifra_sedista"] = sediste

    return sve_karte


"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if broj_karte not in sve_karte:
        raise Exception ("Broj karte nije validan.")

    if korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]["obrisana"] = True
    elif korisnik["uloga"] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        raise Exception ("Korisnik nije validan.")

    return sve_karte

"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: str="",
                             korisnicko_ime_putnika: str="")->list:
    #Lista karata po zadatim kriterijumima
    karte = []
    kriterijumi = {}

    #Ubacivanje kriterijuma u dictionary-je
    if polaziste:
        kriterijumi["sifra_polazisnog_aerodroma"] = polaziste
    if odrediste:
        kriterijumi["sifra_odredisnog_aerodorma"] = odrediste
    if datum_polaska:
        kriterijumi["datum_i_vreme_polaska"] = datum_polaska
    if datum_dolaska:
        kriterijumi["datum_i_vreme_dolaska"] = datum_dolaska
    if korisnicko_ime_putnika:
        kriterijumi["kupac"] = korisnicko_ime_putnika

    for karta in sve_karte.values():
        ispunila = True  #ispunila kriterijume
        for kljuc in kriterijumi:
            if kljuc in karta.keys():
                if karta[kljuc]["uloga"] == konstante.ULOGA_NKORISNIK or karta[kljuc]["korisnicko_ime"] != kriterijumi[kljuc]:
                    ispunila = False
                    break
            if kljuc in svi_konkretni_letovi[karta["sifra_konkretnog_leta"]].keys():
                if svi_konkretni_letovi[karta["sifra_konkretnog_leta"]][kljuc] != kriterijumi[kljuc]:
                    ispunila = False
                    break
            if kljuc in svi_letovi[svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]].keys():
                if svi_letovi[svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["broj_leta"]][kljuc] != kriterijumi[kljuc]:
                    ispunila = False
                    break
        if ispunila:
            karte.append(karta)
            
    return karte

"""
Funkcija koja kreira kartu sa podacima prosledjenim iz fajla
"""
def kreiranje_karte(sve_karte: dict, broj_karte: int, putnici: iter, sifra_konkretnog_leta: int, obrisana: bool,
                    datum_prodaje: str, prodavac: dict, kupac: dict, sifra_sedista: str, status: str = None,) -> dict:
    
    if broj_karte in sve_karte:
        raise Exception ("Karta sa prosleđenom šifrom vec postoji.")

    # Ako je sediste zauzeto izbacuje gresku
    for karta in sve_karte:
        if (sve_karte[karta]["sifra_konkretnog_leta"] == sifra_konkretnog_leta and
            sve_karte[karta]["sifra_sedista"] != "" and sve_karte[karta]["sifra_sedista"] == sifra_sedista):
                raise Exception ("Sediste je zauzeto.")
    
    if len(datum_prodaje) != 11:
        datum_prodaje = datetime.strptime(datum_prodaje,'%Y-%m-%d %H:%M:%S')
    if prodavac:
        prodavac = eval(prodavac)

    karta = {
        "broj_karte": broj_karte,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "kupac": kupac,
        "prodavac": prodavac,
        "sifra_sedista": sifra_sedista,
        "datum_prodaje": datum_prodaje,
        "obrisana": obrisana,
        "putnici": putnici
        }
    if status:
        karta["status"] = status

    sve_karte[broj_karte] = karta
    return sve_karte

"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    fajl = open(putanja,'w')

    # Upis karata u fajl
    for karta in sve_karte:
        if 'status' in  sve_karte[karta].keys():
            fajl.write(str(sve_karte[karta]["broj_karte"]) + separator +
                    str(sve_karte[karta]["putnici"]) + separator +
                    str(sve_karte[karta]["sifra_konkretnog_leta"]) + separator +
                    str(sve_karte[karta]["obrisana"]) + separator +
                    str(sve_karte[karta]["datum_prodaje"]) + separator +
                    str(sve_karte[karta]["prodavac"]) + separator +
                    str(sve_karte[karta]["kupac"]) + separator +
                    str(sve_karte[karta]["sifra_sedista"]) + separator +
                    sve_karte[karta]["status"] + '\n')
        else:
            fajl.write(str(sve_karte[karta]["broj_karte"]) + separator +
                    str(sve_karte[karta]["putnici"]) + separator +
                    str(sve_karte[karta]["sifra_konkretnog_leta"]) + separator +
                    str(sve_karte[karta]["obrisana"]) + separator +
                    str(sve_karte[karta]["datum_prodaje"]) + separator +
                    str(sve_karte[karta]["prodavac"]) + separator +
                    str(sve_karte[karta]["kupac"]) + separator +
                    str(sve_karte[karta]["sifra_sedista"]) + '\n')

    fajl.close()

"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    sve_karte = {}

    # Učitavanje karti iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)

        if len(podaci) == 9:
            sve_karte = kreiranje_karte(sve_karte,eval(podaci[0]),eval(podaci[1]),eval(podaci[2]),eval(podaci[3]),
                                        podaci[4],podaci[5],eval(podaci[6]),podaci[7],podaci[8].strip())
        else:
            sve_karte = kreiranje_karte(sve_karte,eval(podaci[0]),eval(podaci[1]),eval(podaci[2]),eval(podaci[3]),
                                        podaci[4],podaci[5],eval(podaci[6]),podaci[7].strip())

    fajl.close()
    return sve_karte
