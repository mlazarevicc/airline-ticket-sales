
def validan_aerodrom(skracenica: str, pun_naziv: str, grad: str, drzava: str):

    if not skracenica or len(skracenica) != 3:
        raise Exception ("Skracenica aerodroma nije validna")
    if not pun_naziv:
        raise Exception ("Pun naziv aerodroma nije validan.")
    if not grad:
        raise Exception ("Grad nije validan")
    if not drzava:
        raise Exception ("Drzava nije validna")

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(svi_aerodromi: dict, skracenica: str ="", pun_naziv: str ="", grad: str ="", drzava: str ="") -> dict:
    
    if skracenica in svi_aerodromi:
        raise Exception ("Broj leta je zauzet.")
    
    validan_aerodrom(skracenica,pun_naziv,grad,drzava)

    aerodrom = {"skracenica": skracenica,
                "pun_naziv": pun_naziv,
                "grad": grad,
                "drzava": drzava }

    svi_aerodromi[skracenica] = aerodrom
    return svi_aerodromi

"""
Funkcija koja vraca skraceni naziv aerodroma nekog grada
"""
def pronadji_skracenicu_aerodroma(svi_aerodromi: dict, mesto: str):
    for aerodrom in svi_aerodromi.values():
        if aerodrom['grad'].lower() == mesto.lower():
            return aerodrom['skracenica']

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    fajl = open(putanja,'w')

    # Upis aerodroma u fajl
    for aerodrom in svi_aerodromi:
        fajl.write(svi_aerodromi[aerodrom]["skracenica"] + separator +
                   svi_aerodromi[aerodrom]["pun_naziv"] + separator +
                   svi_aerodromi[aerodrom]["grad"] + separator +
                   svi_aerodromi[aerodrom]["drzava"] + '\n')
    
    fajl.close()

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    svi_aerodromi = {}

    # Učitavanje aerodroma iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)

        svi_aerodromi = kreiranje_aerodroma(svi_aerodromi,podaci[0],podaci[1],podaci[2],podaci[3].strip())

    fajl.close()

    return svi_aerodromi