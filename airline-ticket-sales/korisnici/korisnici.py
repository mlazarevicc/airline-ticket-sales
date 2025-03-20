from common import konstante

# Funkcija koja proverava da li su u stringu samo validni znakovi koji se prosleđuju funkciji
#     - podrazumevano je da su slova validna
def validni_znakovi(tekst: str, znakovi: str) -> bool:

    if not tekst.isalpha():
        for znak in tekst:
            if not znak.isalpha():
                if znak not in znakovi:
                    return False
    return True

# Funkcija koja proverava da li je uneti email validan
def validan_email(email: str):
    elementi = email.split('@')
    if len(elementi) == 2:
        if validni_znakovi(elementi[0],'0123456789.-_'):
            elementi = elementi[1].split('.')
            if len(elementi) == 2 and elementi[0].isalpha() and elementi[1].isalpha():
                return True

    return False

# Funkcija koja proverava da li su prosleđeni podaci o korisniku validni
def validan_korisnik(uloga: str, korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                     pasos: str = "", drzavljanstvo: str = "", telefon: str = "", pol: str = ""):

    if uloga not in (konstante.ULOGA_KORISNIK,konstante.ULOGA_ADMIN,konstante.ULOGA_PRODAVAC):
        raise Exception ("Uloga nije validna. Pokušajte ponovo.")

    if not korisnicko_ime:
        raise Exception ("Korisničko ime nije validno. Pokušajte ponovo.")

    if not lozinka or not validni_znakovi(lozinka,'0123456789._- '):
        raise Exception ("Lozinka nije validna. Pokušajte ponovo.")

    if not ime or not validni_znakovi(ime,' '):
        raise Exception ("Ime nije validno. Pokušajte ponovo.")

    if not prezime or not validni_znakovi(prezime,' '):
        raise Exception ("Prezime nije validno. Pokušajte ponovo.")
    
    if not telefon or not telefon.isnumeric():
        raise Exception ("Broj telefona nije validan. Pokušajte ponovo.")

    if not email or not validan_email(email):
        raise Exception ("Email nije validan. Pokušajte ponovo.")

    if pasos:
        if len(pasos) != 9 or not pasos.isnumeric():
            raise Exception ("Broj pasoša nije validan. Pokušajte ponovo.")
    if drzavljanstvo:
        if drzavljanstvo == "" or not validni_znakovi(drzavljanstvo,' '):
            raise Exception ("Državljanstvo nije validno. Pokušajte ponovo.")
    if pol:
        if pol == "" or not validni_znakovi(pol,' '):
            raise Exception ("Pol nije validan. Pokušajte ponovo.")


"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    if azuriraj:
        if staro_korisnicko_ime not in svi_korisnici:
            raise Exception ("Ne postoji korisnik sa unetim korisničkim imenom.")

        # Korisnik sa starim podacima se briše kako bi ubacili istog tog korisnika, samo sa novim podacima
        del svi_korisnici[staro_korisnicko_ime]

    if korisnicko_ime in svi_korisnici:
        raise Exception ("Korisničko ime je zauzeto.")

    # Provera validnosti prosledjenih podataka korisnika
    validan_korisnik(uloga,korisnicko_ime,lozinka,ime,prezime,email,pasos,drzavljanstvo,telefon,pol)

    korisnik = {"uloga": uloga, "korisnicko_ime": korisnicko_ime, "lozinka": lozinka, "ime": ime, "prezime": prezime,
                "email": email, "pasos": pasos, "drzavljanstvo": drzavljanstvo, "telefon": telefon, "pol": pol }

    # Novi korisnik se ubacuje u dictionary svih korisnika
    svi_korisnici[korisnicko_ime] = korisnik
    return svi_korisnici

"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    fajl = open(putanja,'w')

    # Upis korisnika u fajl
    for p_korisnik in svi_korisnici:
        fajl.write(svi_korisnici[p_korisnik]["uloga"] + separator +
                   svi_korisnici[p_korisnik]["korisnicko_ime"] + separator +
                   svi_korisnici[p_korisnik]["lozinka"] + separator +
                   svi_korisnici[p_korisnik]["ime"] + separator +
                   svi_korisnici[p_korisnik]["prezime"] + separator +
                   svi_korisnici[p_korisnik]["email"] + separator +
                   svi_korisnici[p_korisnik]["pasos"] + separator +
                   svi_korisnici[p_korisnik]["drzavljanstvo"] + separator +
                   svi_korisnici[p_korisnik]["telefon"] + separator +
                   svi_korisnici[p_korisnik]["pol"] + '\n')

    fajl.close()

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    fajl = open(putanja,'r')

    svi_korisnici = {}

    # Učitavanje korisnika iz fajla
    for linija in fajl.readlines():
        podaci = linija.split(separator)
        svi_korisnici = kreiraj_korisnika(svi_korisnici,False,podaci[0],"",podaci[1],podaci[2],podaci[3],
                                          podaci[4],podaci[5],podaci[6],podaci[7],podaci[8],podaci[9].strip())

    fajl.close()
    return svi_korisnici


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    
    if korisnicko_ime in svi_korisnici:
        if svi_korisnici[korisnicko_ime]["lozinka"] == lozinka:
            return svi_korisnici[korisnicko_ime]
        raise Exception ("\nUneli ste pogrešnu lozinku. Pokušajte ponovo.\n")

    raise Exception ("\nNe postoji korinsik sa unetim korisničkim imenom.\n")