from datetime import datetime, date, timedelta

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    nerealizovani_letovi = []
    for let in svi_letovi.values():
        if datetime.now() < let["datum_pocetka_operativnosti"]:
            nerealizovani_letovi.append(let)

    return nerealizovani_letovi
"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    #Kriterijum za dva dictionary-ja
    kriterijum = {}

    #Lista konkretnih letova po zadatim kriterijumima
    letovi = []

    #Ubacivanje kriterijuma u dictionary-je
    if polaziste:
        kriterijum["sifra_polazisnog_aerodroma"] = polaziste
    if odrediste:
        kriterijum["sifra_odredisnog_aerodorma"] = odrediste
    if vreme_poletanja:
        kriterijum["vreme_poletanja"] = vreme_poletanja
    if vreme_sletanja:
        kriterijum["vreme_sletanja"] = vreme_sletanja
    if datum_polaska:
        kriterijum["datum_i_vreme_polaska"] = datum_polaska.date()
    if datum_dolaska:
        kriterijum["datum_i_vreme_dolaska"] = datum_dolaska.date()
    if prevoznik:
        kriterijum["prevoznik"] = prevoznik

    if not kriterijum:
        return list(konkretni_letovi.values())

    #Prolaz kroz se letove
    for let in konkretni_letovi.values():
        ispunila = True

        #Proverava se da li let ispunjava kriterijume za dictionary svi_letovi
        for kljuc in kriterijum:
            if (kljuc in svi_letovi[let["broj_leta"]].keys() and svi_letovi[let["broj_leta"]][kljuc] != kriterijum[kljuc]):
                    ispunila = False
                    break
            if kljuc in let.keys() and let[kljuc].date() != kriterijum[kljuc]:
                    ispunila = False
                    break

        if ispunila:
            letovi.append(let)
        
    return letovi

def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):

    #Dictionary koji ce biti u obliku {"broj_leta": cena}
    cene = {}

    for let in svi_letovi:
        if not polaziste or polaziste == svi_letovi[let]["sifra_polazisnog_aerodroma"]:
            if not odrediste or odrediste == svi_letovi[let]["sifra_odredisnog_aerodorma"]:
                cene[let] = svi_letovi[let]["cena"]
    
    #Sortiranje dictionary-ja po vrednosti i pravljenje liste 10 najjeftinijih cena
    cene = list(sorted(cene.items(), key = lambda podatak:podatak[1]))[:10]
    cene = sorted(cene,reverse=True, key = lambda podatak:podatak[1])

    #U listu se smestaju 10 najjeftinijih letova u opadajucem redosledu
    letovi = []
    for let in cene:
        letovi.append(svi_letovi[let[0]])

    return letovi


# Fnukcija koja proverava da li su podaci o letu validni
def validan_let(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str, vreme_poletanja: str,
                vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str, dani: list, model: dict, cena: int,
                datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime):
    
    if not (len(broj_leta) == 4 and broj_leta[:2].isalpha() and broj_leta[2:4].isnumeric()):
        raise Exception ("Neispravan broj leta.")

    if not (sifra_polazisnog_aerodroma.isalpha() and len(sifra_polazisnog_aerodroma) == 3):
        raise Exception ("Niste uneli šifru polazišnog aerodroma.")

    if not (sifra_odredisnog_aerodorma.isalpha() and len(sifra_odredisnog_aerodorma) == 3):
        raise Exception ("Niste uneli šifru odredišnog aerodroma.")

    if not datetime.strptime(vreme_poletanja,'%H:%M'):
        raise Exception ("Nije validno vreme poletanja.")

    if not datetime.strptime(vreme_sletanja,'%H:%M'):
        raise Exception ("Nije validno vreme sletanja.")

    if type(sletanje_sutra) != bool:
        raise Exception ("Tip promenljive 'sletanje_sutra' nije validan.")

    if not prevoznik:
        raise Exception ("Prevoznik nije unet.")

    if not dani or all(dani) not in range(0,7):
        raise Exception ("Dani obavljanja leta nisu validni.")

    if cena <= 0:
        raise Exception ("Cena nije validna.")

    if datum_pocetka_operativnosti > datum_kraja_operativnosti:
        raise Exception ("Datum početka ili kraja operativnosti nije validan.")

    #Provera validnosti podataka o modelu aviona
    if model["id"] < 0:
        raise Exception ("ID aviona nije validan.")

    if not model["naziv"]:
        raise Exception ("Naziv aviona nije validan.")
    
    if model["broj_redova"] <= 0:
        raise Exception ("Broj redova nije validan.")

    if not all(slovo in "ABCDEFGH" for slovo in model["pozicije_sedista"]):
        raise Exception ("Pozicija sedišta nije validna.")

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                     datum_kraja_operativnosti: datetime = None):

    if broj_leta in svi_letovi:
        raise Exception ("Broj leta je zauzet.")
    
    validan_let(broj_leta,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodorma,vreme_poletanja,
    vreme_sletanja,sletanje_sutra,prevoznik,dani,model,cena,datum_pocetka_operativnosti,datum_kraja_operativnosti)

    let = { "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
            "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
            "vreme_poletanja": vreme_poletanja,
            "vreme_sletanja": vreme_sletanja,
            "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
            "datum_kraja_operativnosti": datum_kraja_operativnosti,
            "sletanje_sutra": sletanje_sutra,
            "prevoznik": prevoznik,
            "dani": dani,
            "model": model,
            "cena": cena }

    svi_letovi[broj_leta] = let
    return svi_letovi

"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                  vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str, dani: list, model: dict,
                  cena: float, datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime) -> dict:

    if broj_leta not in svi_letovi:
        raise Exception ("Uneti broj leta ne postoji.")

    validan_let(broj_leta,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodorma,vreme_poletanja,
    vreme_sletanja,sletanje_sutra,prevoznik,dani,model,cena,datum_pocetka_operativnosti,datum_kraja_operativnosti)

    let = { "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
            "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
            "vreme_poletanja": vreme_poletanja,
            "vreme_sletanja": vreme_sletanja,
            "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
            "datum_kraja_operativnosti": datum_kraja_operativnosti,
            "sletanje_sutra": sletanje_sutra,
            "prevoznik": prevoznik,
            "dani": dani,
            "model": model,
            "cena": cena }
        
    del svi_letovi[broj_leta]
    svi_letovi[broj_leta] = let

    return svi_letovi

"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    fajl = open(putanja,'w')

    # Upis letova u fajl
    for p_let in svi_letovi:
        fajl.write(svi_letovi[p_let]["broj_leta"] + separator +
                   svi_letovi[p_let]["sifra_polazisnog_aerodroma"] + separator +
                   svi_letovi[p_let]["sifra_odredisnog_aerodorma"] + separator +
                   svi_letovi[p_let]["vreme_poletanja"] + separator +
                   svi_letovi[p_let]["vreme_sletanja"] + separator +
                   str(svi_letovi[p_let]["sletanje_sutra"]) + separator +
                   svi_letovi[p_let]["prevoznik"] + separator + 
                   str(svi_letovi[p_let]["dani"]) + separator + 
                   str(svi_letovi[p_let]["model"]) + separator +
                   str(svi_letovi[p_let]["cena"]) + separator +
                   str(svi_letovi[p_let]["datum_pocetka_operativnosti"]) + separator +
                   str(svi_letovi[p_let]["datum_kraja_operativnosti"]) + '\n')
    
    fajl.close()

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    svi_letovi = {}

    # Učitavanje letova iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)

        svi_letovi = kreiranje_letova(svi_letovi,podaci[0],podaci[1],podaci[2],podaci[3],podaci[4],eval(podaci[5]),
                                      podaci[6],eval(podaci[7]),eval(podaci[8]),eval(podaci[9]),
                                      datetime.strptime(podaci[10],'%Y-%m-%d %H:%M:%S'),
                                      datetime.strptime(podaci[11].strip(),'%Y-%m-%d %H:%M:%S'))

    fajl.close()

    return svi_letovi

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    
    matrica = []
    avion = svi_letovi[konkretni_let["broj_leta"]]["model"]

    for i in range(avion["broj_redova"]):
        matrica.append([False for j in range(len(avion["pozicije_sedista"]))])
    
    konkretni_let["zauzetost"] = matrica

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretni_let: dict) -> list:
    return konkretni_let["zauzetost"]

"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str): # -> (dict, dict)

    #Provera validnosti unete pozicije sedista za zauzimanje
    avion = svi_letovi[konkretni_let["broj_leta"]]["model"]
    if red > avion["broj_redova"]:
        raise Exception ("Broj reda ne postoji.")
    if pozicija not in avion["pozicije_sedista"]:
        raise Exception ("Pozicija sedista ne postoji.")

    #Promenljiva pomocu koje proveravamo koliko je vremena ostalo do polaska
    razlika = konkretni_let["datum_i_vreme_polaska"] - datetime.now()
    if razlika.total_seconds()/3600 < 48:  # sekunde -> sate 
        raise Exception ("Zakasnili ste sa zauzimanjem sedista.")

    #Provera da li je mesto za zauzimanje zauzeto
    if konkretni_let["zauzetost"][red-1][ord(pozicija)-65]:
        raise Exception ("Mesto je zauzeto.")

    konkretni_let["zauzetost"][red-1][ord(pozicija)-65] = True
    karta["sifra_sedista"] = f"{pozicija}{red}"

    return konkretni_let, karta

"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    
    if konkretni_let["broj_leta"] not in svi_letovi:
        raise Exception ("Prosledjeni let ne postoji")

    letovi = []
    odrediste = svi_letovi[konkretni_let["broj_leta"]]["sifra_odredisnog_aerodorma"]

    for let in svi_konkretni_letovi.values():
        if (svi_letovi[let["broj_leta"]]["sifra_polazisnog_aerodroma"] == odrediste and 
           (let["datum_i_vreme_polaska"] - konkretni_let["datum_i_vreme_dolaska"]) > timedelta(minutes=0) and
           (let["datum_i_vreme_polaska"] - konkretni_let["datum_i_vreme_dolaska"]) < timedelta(minutes=123)):
            letovi.append(let)

    return letovi

"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:

    letovi = []

    for let in konkretni_letovi.values():
        if (let["broj_leta"] in svi_letovi and
            svi_letovi[let["broj_leta"]]["sifra_polazisnog_aerodroma"] == polaziste and 
            svi_letovi[let["broj_leta"]]["sifra_odredisnog_aerodorma"] == odrediste and
            let["datum_i_vreme_polaska"].date() > datum_polaska.date() - timedelta(days=broj_fleksibilnih_dana) and
            let["datum_i_vreme_polaska"].date() < datum_polaska.date() + timedelta(days=broj_fleksibilnih_dana) and
            let["datum_i_vreme_dolaska"].date() > datum_dolaska.date() - timedelta(days=broj_fleksibilnih_dana) and
            let["datum_i_vreme_dolaska"].date() < datum_dolaska.date() + timedelta(days=broj_fleksibilnih_dana)):

            letovi.append(let)

    return letovi