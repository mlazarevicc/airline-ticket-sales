from datetime import datetime, timedelta
from letovi import letovi

def sledeci_broj_leta(letovi: dict):
    broj = 0
    for let in letovi:
        if let > broj: broj = let
    return broj
"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    
    sifra_konkretnog_leta = sledeci_broj_leta(svi_konkretni_letovi)

    #Lista dana ce se prazniti
    for dan in let["dani"]:

        datum = let["datum_pocetka_operativnosti"]
        datum = datum.replace(hour=0, minute=0, second=0)

        #Petlja koja prolazi kroz svaki dan u nedelji dok ne naidje na onaj kojim s obavlja let
        while datum.weekday() != dan:
            datum += timedelta(days=1)

        #Dok se let jos ralizuje
        while datum.date() < let["datum_kraja_operativnosti"].date():
            sifra_konkretnog_leta += 1

            konkretan_let = {
                "sifra": sifra_konkretnog_leta,
                "broj_leta": let["broj_leta"],
                "datum_i_vreme_polaska": datum + timedelta(hours = int(let["vreme_poletanja"].split(":")[0]), minutes = int(let["vreme_poletanja"].split(":")[1])),
                "datum_i_vreme_dolaska": datum + timedelta(hours = int(let["vreme_sletanja"].split(":")[0]), minutes = int(let["vreme_sletanja"].split(":")[1]))
            }

            if let['sletanje_sutra']:
                konkretan_let["datum_i_vreme_dolaska"] += timedelta(days=1)

            #Datum se povecava za sedam dana
            datum += timedelta(days=7)
            svi_konkretni_letovi[sifra_konkretnog_leta] = konkretan_let

    return svi_konkretni_letovi

"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    fajl = open(putanja,'w')

    # Upis letova u fajl
    for p_let in svi_konkretni_letovi:
        fajl.write(str(svi_konkretni_letovi[p_let]["sifra"]) + separator +
                   svi_konkretni_letovi[p_let]["broj_leta"] + separator +
                   str(svi_konkretni_letovi[p_let]["datum_i_vreme_polaska"]) + separator +
                   str(svi_konkretni_letovi[p_let]["datum_i_vreme_dolaska"]) + separator +
                   str(svi_konkretni_letovi[p_let]["zauzetost"]) + '\n')
    
    fajl.close()

"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    svi_konkretni_letovi = {}

    # Učitavanje konkretnih letova iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)

        konkretan_let = {
            "sifra": eval(podaci[0]),
            "broj_leta": podaci[1],
            "datum_i_vreme_polaska": datetime.strptime(podaci[2],'%Y-%m-%d %H:%M:%S'),
            "datum_i_vreme_dolaska": datetime.strptime(podaci[3],'%Y-%m-%d %H:%M:%S'),
            "zauzetost": eval(podaci[4].strip())
        }

        svi_konkretni_letovi[konkretan_let["sifra"]] = konkretan_let

    fajl.close()

    return svi_konkretni_letovi

def konkretni_letovi_letova(svi_konkrenti_letovi: dict, letovi: list) -> list:
    konkretni_letovi = []
    for let in letovi:
        for let2 in svi_konkrenti_letovi.values():
            if let2["broj_leta"] == let["broj_leta"] and let2["datum_i_vreme_polaska"] > datetime.now():
                konkretni_letovi.append(let2)

    return konkretni_letovi