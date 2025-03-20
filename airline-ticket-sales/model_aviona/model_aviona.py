
"""
Brojačka promenljiva koja se automatski povećava pri kreiranju novog modela aviona.
"""
sledeci_broj_modela_aviona = 0

def validan_model_aviona(naziv: str, broj_redova: str, pozicije_sedista: list):
    if not naziv:
        raise Exception ("Naziv modela aviona nije validan")
    if not broj_redova:
        raise Exception ("Broj redova nije validan.")
    if not pozicije_sedista:
        raise Exception ("Pozicije sedista nisu validne")

"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(svi_modeli_aviona: dict, naziv: str ="", broj_redova: str = "", pozicije_sedista: list = []) -> dict:
    
    #Ako model vec postoji izlazi se iz funkcije
    if pronadji_model(svi_modeli_aviona,naziv,broj_redova,pozicije_sedista):
        return svi_modeli_aviona
    
    validan_model_aviona(naziv,broj_redova,pozicije_sedista)
    global sledeci_broj_modela_aviona

    avion = { "id": sledeci_broj_modela_aviona,
              "naziv": naziv,
              "broj_redova": broj_redova,
              "pozicije_sedista": pozicije_sedista }

    svi_modeli_aviona[sledeci_broj_modela_aviona] = avion
    sledeci_broj_modela_aviona += 1
    return svi_modeli_aviona

def pronadji_model(svi_modeli_aviona: dict, naziv: str ="", broj_redova: str = "", pozicije_sedista: list = []) -> dict:

    avion = { "naziv": naziv,
              "broj_redova": broj_redova,
              "pozicije_sedista": pozicije_sedista }
    
    #Provera da li model aviona vec postoji
    for model in svi_modeli_aviona.values():
        avion2 = model.copy()
        del avion2["id"]
        if avion == avion2:
            return model
    return None

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
# Ovde su verovatno misliili svi_modeli_aviona
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    fajl = open(putanja,'w')

    # Upis aerodroma u fajl
    for model in svi_aerodromi:
        fajl.write(str(svi_aerodromi[model]["id"]) + separator +
                   svi_aerodromi[model]["naziv"] + separator +
                   str(svi_aerodromi[model]["broj_redova"]) + separator +
                   str(svi_aerodromi[model]["pozicije_sedista"]) + '\n')
    
    fajl.close()

"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    svi_modeli = {}

    # Učitavanje aerodroma iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)

        svi_modeli[eval(podaci[0])] = {"id": eval(podaci[0]),
                                       "naziv": podaci[1],
                                       "broj_redova": eval(podaci[2]),
                                       "pozicije_sedista": eval(podaci[3].strip())}

    fajl.close()

    return svi_modeli