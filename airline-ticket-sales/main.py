from korisnici import korisnici
from letovi import letovi
from karte import karte
from konkretni_letovi import konkretni_letovi
from izvestaji import izvestaji
from aerodromi import aerodromi
from model_aviona import model_aviona
from common import konstante

import sys
from datetime import date, datetime

trenutno_regisrovan = {"uloga": str, "korisnicko_ime": str, "lozinka": str, "ime": str, "prezime": str,
                       "email": str, "pasos": str, "drzavljanstvo": str, "telefon": str, "pol": str}
svi_korisnici = {}
sve_karte = {}
svi_letovi = {}
svi_konkretni_letovi = {}
svi_aerodromi = {}

def podeli():
    print('-'*40)

def prikazi_letove(letovi: list):

    print("\n  Broj leta    Šifra polazišnog aerodroma    Šifra odredišnog aerodroma   Vreme poletanja  Vreme sletanja        Prevoznik      Cena leta")
    print('-'*140)

    for let in letovi:
        print(f"{let['broj_leta']:^13}{let['sifra_polazisnog_aerodroma']:^30}{let['sifra_odredisnog_aerodorma']:^30}"
              f"{let['vreme_poletanja']:^17}{let['vreme_sletanja']:^17}{let['prevoznik']:^21}{let['cena']:^10.2f}\n")

def prikazi_karte(karte: iter):
    global svi_aerodromi, svi_konkretni_letovi, svi_letovi

    if type(karte) == dict:
        karte = list(karte.values())
    
    print("  Broj karte    Naziv polazišnog aerodroma    Naziv odredišnog aerodroma        Cena         Datum prodaje      Datum polaska           Prodavac             Kupac")
    print('-'*170)

    for karta in karte:
        prodavac = "/"
        datum_prodaje = "/"
        if karta['prodavac']:
            prodavac = karta['prodavac']['ime'] + " " + karta['prodavac']['prezime']
        if karta['datum_prodaje']:
            datum_prodaje = (datetime.strftime(karta['datum_prodaje'],'%Y-%m-%d %H:%S:%M')).split(' ')[0]
        kupac = karta['kupac']['ime'] + " " + karta['kupac']['prezime']
        print(f"{karta['broj_karte']:^14}"
              f"{svi_aerodromi[svi_letovi[svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta']]['sifra_polazisnog_aerodroma']]['pun_naziv']:^30}"
              f"{svi_aerodromi[svi_letovi[svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta']]['sifra_odredisnog_aerodorma']]['pun_naziv']:^30}"
              f"{str(svi_letovi[svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta']]['cena']):^17}{datum_prodaje:^17}"
              f"{str(svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska']):^22}{prodavac:^21}{kupac:^20}\n")

def prikazi_konkretne_letove(konkretni_letovi: list):
    global svi_letovi, svi_aerodromi

    print("  Sifra leta   Naziv polazišnog aerodroma    Naziv odredišnog aerodroma   Datum i vreme polaska   Datum i vreme dolaska")
    print('-'*120)

    for let in konkretni_letovi:
        print(f"{let['sifra']:^13}{svi_aerodromi[svi_letovi[let['broj_leta']]['sifra_polazisnog_aerodroma']]['pun_naziv']:^30}{svi_aerodromi[svi_letovi[let['broj_leta']]['sifra_odredisnog_aerodorma']]['pun_naziv']:^30}"
              f"{str(let['datum_i_vreme_polaska']):^24}{str(let['datum_i_vreme_dolaska']):^24}\n")

def prikazi_korisnike(korisnici: list):
    
    print("    Korisničko ime       Ime        Prezime             Email              Broj telefona       Pol")
    print('-'*110)

    for korisnik in korisnici:
        print(f"{korisnik['korisnicko_ime']:^22}{korisnik['ime']:^10}{korisnik['prezime']:^16}{korisnik['email']:^22}{korisnik['telefon']:^24}{korisnik['pol']:^5}\n")

def prikazi_neregistrovane(korisnici: list):
    print("     Ime        Prezime             Email               Broj telefona")
    print('-'*70)

    for korisnik in korisnici:
        print(f"{korisnik['ime']:^12}{korisnik['prezime']:^16}{korisnik['email']:^22}{korisnik['telefon']:^24}\n")

def prikazi_opcije(tip_korisnika: str):

    if tip_korisnika == "neregistrovan":
        print("\n     -- Dobrodošli --\n\n"
              "Izaberite željenu radnju:\n"
              "  1. Prijava na sistem\n"
              "  2. Registracija\n"
              "  3. Pregled nerealizovanih letova\n"
              "  4. Pretraga letova\n"
              "  5. Višekriterijumska pretraga letova\n"
              "  6. 10 najjeftinijih letova\n"
              "  7. Fleksibilni polasci za odredjeno mesto i datum\n"
              "  8. Izlazak iz aplikacije")

    elif tip_korisnika == "registrovani_kupac":
        print("Izaberite zeljenu radnju:\n"
              "  1. Kupovina karata\n"
              "  2. Pregled nerealizovanih karata\n"
              "  3. Prijava na let\n"
              "  4. Pretraga letova\n"
              "  5. Višekriterijumska pretraga letova\n"
              "  6. 10 najjeftinijih letova\n"
              "  7. Fleksibilni polasci za odredjeno mesto i datum\n"
              "  8. Odjava sa sitema\n"
              "  9. Izlazak iz aplikacije")

    elif tip_korisnika == "prodavac":
        print("Izaberite zeljenu radnju:\n"
              "  1. Prodaja karata\n"
              "  2. Izmena karte\n"
              "  3. Brisanje karte\n"
              "  4. Pretraga prodatih karata\n"
              "  5. Prijava na let\n"
              "  6. Pregled nerealizovanih letova\n"
              "  7. Pretraga letova\n"
              "  8. Višekriterijumska pretraga letova\n"
              "  9. 10 najjeftinijih letova\n"
              "  10. Fleksibilni polasci za odredjeno mesto i datum\n"
              "  11. Odjava sa sitema\n"
              "  12. Izlazak iz aplikacije")

    elif tip_korisnika == "menadzer":
        print("Izaberite zeljenu radnju:\n"
              "  1. Pretraga prodatih karata\n"
              "  2. Registracija novih prodavaca\n"
              "  3. Kreiranje letova\n"
              "  4. Izmena letova\n"
              "  5. Brisanje karata\n"
              "  6. Izvestaji o kartama\n"
              "  7. Pregled nerealizovanih letova\n"
              "  8. Pretraga letova\n"
              "  9. Višekriterijumska pretraga letova\n"
              "  10. 10 najjeftinijih letova\n"
              "  11. Fleksibilni polasci za odredjeno mesto i datum\n"
              "  12. Odjava sa sitema\n"
              "  13. Izlazak iz aplikacije")

#'Datum i vreme' u 'datum'
def div_u_datum(letovi: dict):
    if type(list(letovi.values())[0]["datum_pocetka_operativnosti"]) == date:
        return letovi
    for let in letovi.values():
        let["datum_pocetka_operativnosti"] = let["datum_pocetka_operativnosti"].date()
        let["datum_kraja_operativnosti"] = let["datum_kraja_operativnosti"].date()
    return letovi
#'Datum' u 'datum i vreme'
def datum_u_div(letovi: dict):
    if type(list(letovi.values())[0]["datum_pocetka_operativnosti"]) == datetime:
        return letovi
    for let in letovi.values():
        let["datum_pocetka_operativnosti"] = datetime.strptime(str(let["datum_pocetka_operativnosti"]) + " 00:00:00",'%Y-%m-%d %H:%M:%S')
        let["datum_kraja_operativnosti"] = datetime.strptime(str(let["datum_kraja_operativnosti"]) + " 00:00:00",'%Y-%m-%d %H:%M:%S')
    return letovi

def validan_datum(datum: str, vreme: bool):
    try:
        if vreme:
            datum2 = datetime.strptime(datum,'%Y-%m-%d %H:%M:%S')
        else:
            datum2 = datetime.strptime(datum,'%Y-%m-%d')
    except Exception as greska:
        datum2 = False
    
    if not datum2:
        raise Exception ("\nFormat datuma nije validan.\n")
    return datum2
    

def registracija(menadzer: bool):
    global svi_korisnici

    while 1:
        try:
            print("Unesite podatke:")
            korisnicko_ime = input("   Korisniško ime: ")
            lozinka =        input("   Lozinka: ")
            ime =            input("   Ime: ")
            prezime =        input("   Prezime: ")
            telefon =        input("   Broj telefona: ")
            email =          input("   Email: ")
            pasos =          input("   Broj pasoša: ")
            drzavljanstvo =  input("   Državljanstvo: ")
            pol =            input("   Pol (npr. M/Z): ")

            if menadzer:
                svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici,False,konstante.ULOGA_PRODAVAC,None,korisnicko_ime,
                                                            lozinka,ime,prezime,email,pasos,drzavljanstvo,telefon,pol)
            else:
                svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici,False,konstante.ULOGA_KORISNIK,None,korisnicko_ime,lozinka,
                                                            ime,prezime,email,pasos,drzavljanstvo,telefon,pol)
            break

        except Exception as greska:
            print(greska)

    korisnici.sacuvaj_korisnike("korisnici.csv",'|',svi_korisnici)
    print("\nRegistracija je uspešna.\n")

def pretraga_letova(kriterijumi: bool):

    global svi_letovi, svi_konkretni_letovi
    if not svi_letovi:
        raise Exception ("Nema letova za pretraživanje.")

    if kriterijumi:
        print("Unesite kriterijume za pretragu letova:\n")
        polaziste =       input("   Mesto polaska: ")
        dolaziste =       input("   Mesto dolaska: ")
        datum_polaska =   input("   Datum polaska (format: 'yyyy-mm-dd'): ")
        datum_dolaska =   input("   Datum dolaska (format: 'yyyy-mm-dd'): ")
        vreme_poletanja = input("   Vreme poletanja: ")
        vreme_sletanja  = input("   Vreme sletanja: ")
        prevoznik =       input("   Prevoznik: ")
    
        if datum_polaska:
            datum_polaska = validan_datum(datum_polaska,False)
        if datum_dolaska:
            datum_dolaska = validan_datum(datum_dolaska,False)

        letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,dolaziste,
                         datum_polaska,datum_dolaska,vreme_poletanja,vreme_sletanja,prevoznik)

    else:
        print("Izaberite kriterijum za pretragu letova:\n"
              "   1. Mesto polaska\n"
              "   2. Mesto dolaska\n"
              "   3. Datum polaska\n"
              "   4. Datum dolaska\n"
              "   5. Vreme poletanja\n"
              "   6. Vreme sletanja\n"
              "   7. Prevoznik")
        kriterijum = input("Izberite opciju: ")

        if kriterijum == '1':
            a = input("Unesite mesto polaska: ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste=a)
        elif kriterijum == '2':
            a = input("Unesite mesto dolaska: ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,odrediste=a)
        elif kriterijum == '3':
            a = input("Unesite datum polaska (format: 'yyyy-mm-dd'): ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,datum_polaska=validan_datum(a,False))
        elif kriterijum == '4':
            a = input("Unesite datum dolaska (format: 'yyyy-mm-dd'): ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,datum_dolaska=validan_datum(a,False))
        elif kriterijum == '5':
            a = input("Unesite vreme poletanja: ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,vreme_poletanja=a)
        elif kriterijum == '6':
            a = input("Unesite vreme sletanja: ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,vreme_sletanja=a)
        elif kriterijum == '7':
            a = input("Unesite naziv prevoznika: ")
            letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,prevoznik=a)

    print()
    if not letovi2:
        raise Exception ("\nNema letova za izabrani kriterijum.\n")
    prikazi_konkretne_letove(letovi2)

def top10():
    global svi_aerodromi, svi_letovi

    polaziste = input("\nUnesite mesto polaska: ")
    odrediste = input("Unesite mesto dolaska: ")

    print("\n  - TOP 10 NAJJEFTNIJIH LETOVA - \n\n")

    letovi2 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi,polaziste,odrediste)

    prikazi_letove(letovi2)

def fleksibilni_polasci():
    global svi_letovi, svi_aerodromi, svi_konkretni_letovi
    if not svi_letovi:
        raise Exception ("Nema letova za pretraživanje.")

    print("Unesite kriterijume za planirani let (svi podaci su obavezni):\n")
    datum_polaska =   input("   Datum polaska (format: 'yyyy-mm-dd'): ")
    datum_dolaska =   input("   Datum dolaska (format: 'yyyy-mm-dd'): ")
    polaziste =       input("   Mesto polaska: ")
    odrediste =       input("   Mesto dolaska: ")
    broj_dana =  eval(input("   Broj fleksibilnih dana oko datuma polaska: "))

    if not (broj_dana and datum_polaska and datum_dolaska and  polaziste and odrediste):
        raise Exception("\nSvi podaci su obavezni.")

    datum_polaska = validan_datum(datum_polaska,False)
    datum_dolaska = validan_datum(datum_dolaska,False)

    print("\n   - FLEKSIBILNI POLASCI -\n\n")

    letovi2 = letovi.fleksibilni_polasci(svi_letovi,svi_konkretni_letovi,polaziste,odrediste,
                                         datum_polaska,broj_dana,datum_dolaska)
    
    prikazi_konkretne_letove(letovi2)

def izlaz():
    global svi_letovi
    karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
    svi_letovi = datum_u_div(svi_letovi)
    letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
    konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi)
    korisnici.sacuvaj_korisnike("korisnici.csv",'|',svi_korisnici)
    sys.exit(0)

def main():
    while 1:
        try:
            prikazi_opcije("neregistrovan")
            print("-" * 40)

            opcija = input("Izaberite opciju: ")
            print("-" * 40)

            if opcija == '1':
                login()
            elif opcija == '2':
                print("\n    - REGISTRACIJA -\n")
                registracija(0)
            elif opcija == '3':
                global svi_letovi
                svi_letovi2 = datum_u_div(svi_letovi.copy())
                letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
                prikazi_letove(letovi2)
            elif opcija == '4':
                pretraga_letova(0)
            elif opcija == '5':
                pretraga_letova(1)
            elif opcija == '6':
                top10()
            elif opcija == '7':
                fleksibilni_polasci()
            elif opcija == '8':
                izlaz()
            else:
                raise Exception ("Unesite validnu radnju!")
        except Exception as greska:
            print(greska)


def login():
    global svi_korisnici, trenutno_regisrovan

    while 1:
        try:
            korisnicko_ime = input("Unesite korisničko ime: ")
            lozinka = input("Unesite lozinku: ")

            korisnik = korisnici.login(svi_korisnici,korisnicko_ime,lozinka)
            trenutno_regisrovan = korisnik

            if korisnik["uloga"] == konstante.ULOGA_KORISNIK:
                print("\nUspešno ste se prijavili kao korisnik.\n")
                korisnik_meni()
                break
            elif korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
                print("\nUspešno ste se prijavili kao prodavac.\n")
                prodavac_meni()
                break
            else:
                print("\nUspešno ste se prijavili kao admin.\n")
                admin_meni()
                break

        except Exception as greska:
            print(greska)

def kupovina_karte(karta: dict = None):
    global svi_konkretni_letovi, svi_letovi, sve_karte
    let = {}

    print("    - KUPOVINA KARATA -\n")
    if not karta:
        
        print("Mogućnosti odabira leta:\n"
              "   1. Preko broja leta\n"
              "   2. Preko podataka o letu")
        a = input("Izaberite opciju: ")

        potvrda = input("Da li želite pogledati listu letova? [da/ne]: ")
        if potvrda.lower() == 'da':
            print()
            svi_letovi2 = datum_u_div(svi_letovi.copy())
            letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
            konkretni_letovi2 = konkretni_letovi.konkretni_letovi_letova(svi_konkretni_letovi,letovi2)
            prikazi_konkretne_letove(konkretni_letovi2)

        #Inicijalizacija potrevnih promenljivih
        letovi2 = []
        broj_leta = 0

        if a == '1':
            broj_leta = eval(input("Unesite broj leta: "))
            if broj_leta not in svi_konkretni_letovi: raise Exception ("Broj leta nije validan.")
            let = svi_konkretni_letovi[broj_leta]
        elif a == '2':
            while 1:
                print("\nUnesite podatke o izabranom letu:\n")
                polaziste =       input("   Mesto polaska: ")
                dolaziste =       input("   Mesto dolaska: ")
                datum_polaska =   input("   Datum polaska (format: 'yyyy-mm-dd hh:mm'): ")
                datum_dolaska =   input("   Datum dolaska (format: 'yyyy-mm-dd hh:mm'): ")
                prevoznik =       input("   Prevoznik: ")

                if datum_polaska:
                    datum_polaska = validan_datum(datum_polaska + ":00",True)
                if datum_dolaska:
                    datum_dolaska = validan_datum(datum_dolaska + ":00",True)

                letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,dolaziste,
                                                 datum_polaska,datum_dolaska,None,None,prevoznik)
            
                if not letovi2:
                    print("\nIzabrani let ne postoji. Pokušajte ponovo.\n")
                elif len(letovi2) > 1:
                    print("\nMorate uneti sve podatke o letu.")
                else:
                    let = letovi2[0]
                    break
        else:
            raise Exception ("Nevalidna radnja.")
            
        broj_karata = eval(input("\nBroj karata za kupovinu: "))

        if broj_karata < 1:
            return
        
        global trenutno_regisrovan
        putnici = [trenutno_regisrovan]

        if broj_karata > 1:
            print("\nUnesite potrebne podatke za ostale putnike:")
            for i in range(broj_karata-1):
                putnik = {}
                while 1:
                    print(f"Saputnik {i+1}:")
                    ime =     input("   Ime: ")
                    prezime = input("   Prezime: ")

                    if not (ime and prezime):
                        print("Podaci nisu validni. Pokušajte ponovo.")
                    else:
                        putnik["ime"] = ime
                        putnik["prezime"] = prezime
                        break

                putnici.append(putnik)

        print("\n  - Potvrda kupovine - \n\n")
        print("Izabrani let: \n")
        prikazi_konkretne_letove([let])
        print("\nVaši podaci:\n")
        prikazi_korisnike([trenutno_regisrovan])
        if len(putnici)>1:
            print("Podaci ostalih putnika:\n")
            print("     Ime         Prezime")
            print('-'*30)
            for putnik in putnici[1:]:
                print(f"{putnik['ime']:^13}{putnik['prezime']:^15}\n")
        
        y = input("Potvrdite kartu [da/ne]: ")

        if y.lower() != 'da':
            return
        
        #Da bi radili testovi broj nove karte je najveci broj koji je vec postoji, pa kartu sa tim brojem cuvamo da bi
        #je na kraju vratili
        broj = karte.sledeci_broj_karte2(sve_karte)
        karta_pomocna = sve_karte[broj]

        datum = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        karta2, sve_karte = karte.kupovina_karte(sve_karte,svi_konkretni_letovi,let["sifra"],putnici,let["zauzetost"],trenutno_regisrovan,
                                                 datum_prodaje = datetime.strptime(datum,'%Y-%m-%d %H:%M:%S'))
        sve_karte[karta2["broj_karte"]]["sifra_sedista"] = ""
        sve_karte[karta2["broj_karte"]]["broj_karte"] = broj+1
        sve_karte[broj], sve_karte[broj+1] = karta_pomocna, karta2

        karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
        print("\nUspešno ste kupili kartu.\n")
        y = input("Da li želite nastaviti sa kupovinom karte za neki povezani let? [da/ne]: ")

        if y.lower() == 'da':
            kupovina_karte(karta2)
    else:
        podeli()
        print("Lista povezanih letova:\n")
        letovi2 = letovi.povezani_letovi(svi_letovi,svi_konkretni_letovi,svi_konkretni_letovi[karta['sifra_konkretnog_leta']])
        if not letovi2:
            raise Exception ("Nema poveznih letova.\n")
            
        prikazi_konkretne_letove(letovi2)

        print("Mogućnosti odabira leta:\n"
              "   1. Preko broja leta\n"
              "   2. Preko podataka o letu")
        a = input("Izaberite opciju: ")

        broj_leta = 0

        if a == '1':
            broj_leta = eval(input("Unesite broj leta: "))
            if broj_leta not in svi_konkretni_letovi: raise Exception ("Broj leta nije validan.")
            let = svi_konkretni_letovi[broj_leta]
        elif a == '2':
            while 1:
                print("\nUnesite podatke o izabranom letu:\n")
                polaziste =       input("   Mesto polaska: ")
                dolaziste =       input("   Mesto dolaska: ")
                datum_polaska =   input("   Datum polaska (format: 'yyyy-mm-dd hh:mm'): ")
                datum_dolaska =   input("   Datum dolaska (format: 'yyyy-mm-dd hh:mm'): ")
                prevoznik =       input("   Prevoznik: ")

                if datum_polaska:
                    datum_polaska = validan_datum(datum_polaska + ":00",True)
                if datum_dolaska:
                    datum_dolaska = validan_datum(datum_dolaska + ":00",True)

                letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,dolaziste,
                                                 datum_polaska,datum_dolaska,None,None,prevoznik)
            
                if not letovi2:
                    print("\nIzabrani let ne postoji. Pokušajte ponovo.\n")
                elif len(letovi2) > 1:
                    print("\nMorate uneti sve podatke o letu.")
                else:
                    let = letovi2[0]
                    break
        else:
            raise Exception ("Nevalidna radnja.")

        broj = karte.sledeci_broj_karte2(sve_karte)
        karta_pomocna = sve_karte[broj]

        datum = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        karta2, sve_karte = karte.kupovina_karte(sve_karte,svi_konkretni_letovi,let["sifra"],karta['putnici'],let['zauzetost'],trenutno_regisrovan,
                                                 datum_prodaje = datetime.strptime(datum,'%Y-%m-%d %H:%M:%S'))

        sve_karte[karta2["broj_karte"]]["sifra_sedista"] = ""
        sve_karte[karta2["broj_karte"]]["broj_karte"] = broj+1
        sve_karte[broj], sve_karte[broj+1] = karta_pomocna, karta2

        karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
        print("\nUšpesno ste kupili kartu.\n")
        y = input("Da li želite nastaviti sa kupovinom karte za neki povezani let? [da/ne]: ")

        if y.lower() == 'da':
            kupovina_karte(karta2)

def prijava_na_let(prodavac: bool, karta: dict = None):
    global trenutno_regisrovan, sve_karte, svi_letovi, svi_konkretni_letovi
    let = {}

    if karta:
        podeli()
        print("Lista povezanih letova:\n")
        letovi2 = letovi.povezani_letovi(svi_letovi,svi_konkretni_letovi,svi_konkretni_letovi[karta['sifra_konkretnog_leta']])
        if not letovi2:
            raise Exception ("Nema poveznih letova.")
            
        karte2 = []
        for karta3 in sve_karte.values():
            if karta3["sifra_konkretnog_leta"] in (let3["sifra"] for let3 in letovi2) and karta3["kupac"] == karta["kupac"]:
                karte2.append(karta3)

        if not karte2:
            raise Exception ("Nije kupljena karta za neki povezani let.")
        prikazi_karte(karte2)

        broj_karte = eval(input("Unesite broj karte za let na koji se prijavljujete: "))
        if broj_karte not in sve_karte:
            raise Exception ("Broj karte nije validan.")
        let = svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]
        
        print("\n  Odabir sedišta:\n('x' znaci da je sediste zauzeto)\n")

        while 1:
            try:
                print()
                for i in range(len(let["zauzetost"])):
                    red = f"Red {i+1}:  "
                    for j in range(len(let["zauzetost"][i])):
                        if let['zauzetost'][i][j]:
                            red += "x "
                        else:
                            red += f"{chr(j+65)} "
                    print(red)

                red = eval(input("\nBroj reda: "))
                kolona = input("Oznaka sedišta: ")
                
                let, karta2 = letovi.checkin(sve_karte[broj_karte],svi_letovi,let,red,kolona)
                sve_karte[broj_karte] = karta2
                break
                
            except Exception as greska:
                print(greska)

    else:
        print("Mogućnosti odabira karte:\n"
                "   1. Preko broja karte\n"
                "   2. Preko podataka o karti")
        a = input("Izaberite opciju: ")
        print()

        #Inicijalizacija potrebnih promenljivih
        broj_karte = 0
        ime = None

        if a == '1':
            if prodavac:
                ime, prezime = input("Unesite ime i prezime kupca: ").split(' ')
                karte2 = []
                for p_karta in sve_karte.values():
                    if p_karta["kupac"]["ime"].lower() == ime.lower() and p_karta["kupac"]["prezime"].lower() == prezime.lower():
                        karte2.append(p_karta)
                if not karte2:
                    raise Exception ("Karta nije pronađena.")
            else:
                ime = trenutno_regisrovan["korisnicko_ime"]
                karte2 = karte.pretraga_prodatih_karata(sve_karte,svi_letovi,svi_konkretni_letovi,None,None,None,None,ime)
            if not karte2:
                raise Exception ("Niste kupili kartu.")
            prikazi_karte(karte2)
            broj_karte = eval(input("Unesite broj karte za let na koji se prijavljujete: "))
            if broj_karte not in sve_karte:
                raise Exception ("Broj karte nije validan.")
            kupac = sve_karte[broj_karte]["kupac"]
            let = svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]
        elif a == '2':
            print("Unesite potrebne podatke:")
            if prodavac:
                ime =     input("   Ime kupca: ")
                prezime = input("   Prezime kupca: ")
            else:
                ime =     input("   Vaše ime: ")
                prezime = input("   Vaše prezime: ")
            polazak =   input("   Mesto polaska: ")
            dolazak =   input("   Mesto dolaska: ")
            datum =     input("   Datum polaska (format: 'yyyy-mm-dd'): ")
            vreme =     input("   Vreme polaska (format: 'hh:mm'): ")

            if not (ime and polazak and dolazak and datum and vreme):
                raise Exception ("Morate uneti sve podatke.")
            if not prodavac and (ime != trenutno_regisrovan["ime"] or prezime != trenutno_regisrovan["prezime"]):
                raise Exception ("Pogrešno korisničko ime.")

            if datum:
                datum = validan_datum(datum + " " + vreme + ":00",True)

            karte2 = karte.pretraga_prodatih_karata(sve_karte,svi_letovi,svi_konkretni_letovi,polazak,dolazak,datum)
            if not karte2:
                raise Exception ("Karta nije pronađena.")

            karte3 = []
            for p_karta in karte2:
                if p_karta["kupac"]["ime"].lower() == ime.lower() and p_karta["kupac"]["prezime"].lower() == prezime.lower():
                    karte3.append(p_karta)
            if not karte3:
                raise Exception ("Karta nije pronađena.")
            prikazi_karte(karte3)

            broj_karte = eval(input("Unesite broj Vaše karte: "))
            if broj_karte not in (p_karta["broj_karte"] for p_karta in karte3):
                raise Exception ("Broj karte nije validan.")
            
            let = svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]
            kupac = sve_karte[broj_karte]["kupac"]
        else:
            raise Exception ("Nevalidna radnja.")

        if len(kupac.keys()) != 5:
            if prodavac:
                if not kupac["pasos"]:
                    pasos = input("\nUnesite broj pasoša kupca: ")
                    if len(pasos) != 9:
                        raise Exception ("\nBroj pasoša nije validan.\n")
                    kupac["pasos"] = pasos
                if not kupac["drzavljanstvo"]:
                    kupac["drzavljanstvo"] = input("Unesite državljanstvo kupca: ")
                if not kupac["pol"]:
                    kupac["pol"] = input("Unesite pol kupca (M/Z): ")
            else:
                if not kupac["pasos"]:
                    pasos = input("\nUnesite broj Vašeg pasosa: ")
                    if len(pasos) != 9:
                        raise Exception ("\nBroj pasoša nije validan.\n")
                    kupac["pasos"] = pasos
                if not kupac["drzavljanstvo"]:
                    kupac["drzavljanstvo"] = input("Unesite Vaše državljanstvo: ")
                if not kupac["pol"]:
                    kupac["pol"] = input("Unesite Vaš pol (M/Z): ")
            svi_korisnici[kupac["korisnicko_ime"]] = kupac
            korisnici.sacuvaj_korisnike('korisnici.csv','|',svi_korisnici)

        print("\n  Odabir sedišta:\n'x' znaci da je sediste zauzeto)\n")

        while 1:
            try:
                print()
                for i in range(len(let["zauzetost"])):
                    red = f"Red {i+1}:  "
                    for j in range(len(let["zauzetost"][i])):
                        if let['zauzetost'][i][j]:
                            red += "x "
                        else:
                            red += f"{chr(j+65)} "
                    print(red)

                red = eval(input("\nBroj reda: "))
                kolona = input("Oznaka sedišta: ")
                
                let, karta2 = letovi.checkin(sve_karte[broj_karte],svi_letovi,let,red,kolona)
                sve_karte[broj_karte] = karta2
                break
                
            except Exception as greska:
                print(greska)
                if greska == 'Zakasnili ste sa zauzimanjem sedista.':
                    return

    konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi)
    karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
    print("\nUspešno ste se prijavili na let.\n")

    letovi2 = letovi.povezani_letovi(svi_letovi,svi_konkretni_letovi,let)
    if letovi2:
        y = input("Da li se želite prijaviti na neki povezani let? [da/ne]: ")
        if y.lower() == 'da':
            prijava_na_let(letovi2,sve_karte[broj_karte])


def korisnik_meni():
    global trenutno_regisrovan, svi_letovi, svi_korisnici, svi_konkretni_letovi, sve_karte
    while 1:
        try:
            prikazi_opcije("registrovani_kupac")

            podeli()
            opcija = input("Izaberite opciju: ")
            podeli()

            if opcija == '1':
                kupovina_karte()
            elif opcija == '2':
                print("      - PREGLED NEREALIZOVANIH KARATA -\n")
                karte2 = karte.pregled_nerealizovanaih_karata(trenutno_regisrovan,list(sve_karte.values()))
                if not karte2:
                    raise Exception ("Korisnik nema kupljenih karata.")
                prikazi_karte(karte2)
            elif opcija == '3':
                print("\n      - PRIJAVA NA LET -\n")
                prijava_na_let(0)
            elif opcija == '4':
                pretraga_letova(0)
            elif opcija == '5':
                pretraga_letova(1)
            elif opcija == '6':
                top10()
            elif opcija == '7':
                fleksibilni_polasci()
            elif opcija == '8':
                trenutno_regisrovan = None
                karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
                svi_letovi = datum_u_div(svi_letovi)
                letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
                svi_letovi = div_u_datum(svi_letovi)
                konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi)
                korisnici.sacuvaj_korisnike("korisnici.csv",'|',svi_korisnici)
                break
            elif opcija == '9':
                izlaz()
            else:
                print("Unesite validnu radnju!\n")
    
        except Exception as greska:
            print(greska)


def prodaja_karte(karta: dict = None):
    global svi_konkretni_letovi, svi_letovi, svi_korisnici, sve_karte

    if not karta:

        print("Mogućnosti odabira leta:\n"
              "   1. Preko broja leta\n"
              "   2. Preko podataka o letu")
        a = input("Izaberite opciju: ")

        potvrda = input("\nDa li želite pogledati listu letova? [da/ne]: ")

        if potvrda.lower() == 'da':
            print()
            svi_letovi2 = datum_u_div(svi_letovi.copy())
            letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
            konkretni_letovi2 = konkretni_letovi.konkretni_letovi_letova(svi_konkretni_letovi,letovi2)
            prikazi_konkretne_letove(konkretni_letovi2)
        
        #Inicijalizacija potrebnih promenljivih
        letovi2 = []
        broj_leta = 0

        if a == '1':
            broj_leta = eval(input("Unesite broj leta: "))
            if broj_leta not in svi_konkretni_letovi: raise Exception ("Broj leta nije validan.")
            let = svi_konkretni_letovi[broj_leta]
        elif a == '2':
            while 1:
                print("\nUnesite podatke o izabranom letu:\n")
                polaziste =       input("   Mesto polaska: ")
                dolaziste =       input("   Mesto dolaska: ")
                datum_polaska =   input("   Datum i vreme polaska (format: 'yyyy-mm-dd hh:mm'): ")
                datum_dolaska =   input("   Datum i vreme dolaska (format: 'yyyy-mm-dd hh:mm'): ")
                prevoznik =       input("   Prevoznik: ")

                if datum_polaska:
                    datum_polaska = validan_datum(datum_polaska + ":00",True)
                if datum_dolaska:
                    datum_dolaska = validan_datum(datum_dolaska + ":00",True)

                letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,dolaziste,
                                                 datum_polaska,datum_dolaska,None,None,prevoznik)
            
                if not letovi2:
                    print("\nIzabrani let ne postoji. Pokušajte ponovo.\n")
                elif len(letovi2) > 1:
                    print("\nMorate uneti sve podatke o letu.")
                else:
                    let = letovi2[0]
                    break
        else:
            raise Exception ("Nevalidna radnja.")

        registrovan = input("Da li je kupac registrovan? [da/ne]: ")
        kupac = None

        if registrovan == 'da':
            while 1:
                korisnicko_ime = input("Unesite korisničko ime kupca: ")
                if korisnicko_ime not in svi_korisnici:
                    raise Exception ("Korisnik ne postoji.")
                kupac = svi_korisnici[korisnicko_ime]

                print()
                prikazi_korisnike([kupac])
                y = input("Da li su ovo podaci Vašeg kupca? [da/ne]: ")
                print()
                if y == 'da':
                    break
        else:
            print("\nUnesite podatke o kupcu:")
            ime =           input("   Ime: ")
            prezime =       input("   Prezime: ")
            telefon =       input("   Broj telefona: ")
            email =         input("   Email: ")
            kupac = {'ime': ime, 'prezime': prezime, 'telefon': telefon, 'email': email, 'uloga': konstante.ULOGA_NKORISNIK}

        broj_karata = eval(input("\nBroj karata za kupovinu: "))

        if broj_karata < 1:
                return

        putnici = [kupac]
        if broj_karata > 1:
            print("\nUnesite potrebne podatke za ostale putnike:")
            for i in range(broj_karata-1):
                putnik = {}
                while 1:
                    print(f"Saputnik {i+1}:")
                    ime =     input("   Ime: ")
                    prezime = input("   Prezime: ")

                    if not (ime and prezime):
                        print("Podaci nisu validni. Pokušajte ponovo.")
                    else:
                        putnik["ime"] = ime
                        putnik["prezime"] = prezime
                        break

                putnici.append(putnik)

        print("\n  - Potvrda kupovine - \n\n")
        print("Izabrani let: \n")
        prikazi_konkretne_letove([let])
        print("\nPodaci kupca:\n")
        if registrovan == 'da':
            prikazi_korisnike([kupac])
        else:
            prikazi_neregistrovane([kupac])
        if len(putnici)>1:
            print("Podaci ostalih putnika:\n")
            print("     Ime        Prezime")
            print('-'*30)
            for putnik in putnici[1:]:
                print(f"{putnik['ime']:^12}{putnik['prezime']:^15}\n")
        
        y = input("Potvrdite kartu [da/ne]: ")

        if y.lower() != 'da':
            return
        
        #Da bi radili testovi broj nove karte je najveci broj koji je vec postoji, pa kartu sa tim brojem cuvamo da bi
        #je na kraju vratili
        broj = karte.sledeci_broj_karte2(sve_karte)
        karta_pomocna = sve_karte[broj]

        datum = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        karta2, sve_karte = karte.kupovina_karte(sve_karte,svi_konkretni_letovi,let["sifra"],putnici,let["zauzetost"],kupac,
                                                datum_prodaje = datetime.strptime(datum,'%Y-%m-%d %H:%M:%S'), prodavac = trenutno_regisrovan)

        sve_karte[karta2["broj_karte"]]["sifra_sedista"] = ""
        sve_karte[karta2["broj_karte"]]["broj_karte"] = broj+1
        sve_karte[broj], sve_karte[broj+1] = karta_pomocna, karta2

        karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
        print("\nUspešno ste prodali kartu.\n")

        y = input("Da li zelite nastaviti sa prodajom karata za neki povezani let? [da/ne]: ")
        if y.lower() == 'da':
            prodaja_karte(karta2)
    else:
        podeli()
        print("Lista povezanih letova:\n")
        letovi2 = letovi.povezani_letovi(svi_letovi,svi_konkretni_letovi,svi_konkretni_letovi[karta['sifra_konkretnog_leta']])
        if not letovi2:
            raise Exception ("Nema poveznih letova.\n")
        prikazi_konkretne_letove(letovi2)

        print("Mogućnosti odabira leta:\n"
              "   1. Preko broja leta\n"
              "   2. Preko podataka o letu")
        a = input("Izaberite opciju: ")

        broj_leta = 0

        if a == '1':
            broj_leta = eval(input("Unesite broj leta: "))
            if broj_leta not in svi_konkretni_letovi: raise Exception ("Broj leta nije validan.")
            let = svi_konkretni_letovi[broj_leta]
        elif a == '2':
            while 1:
                print("\nUnesite podatke o izabranom letu:\n")
                polaziste =       input("   Mesto polaska: ")
                dolaziste =       input("   Mesto dolaska: ")
                datum_polaska =   input("   Datum polaska (format: 'yyyy-mm-dd hh:mm'): ")
                datum_dolaska =   input("   Datum dolaska (format: 'yyyy-mm-dd hh:mm'): ")
                prevoznik =       input("   Prevoznik: ")

                if datum_polaska:
                    datum_polaska = validan_datum(datum_polaska + ":00",True)
                if datum_dolaska:
                    datum_dolaska = validan_datum(datum_dolaska + ":00",True)

                letovi2 = letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,dolaziste,
                                                 datum_polaska,datum_dolaska,None,None,prevoznik)
            
                if not letovi2:
                    print("\nIzabrani let ne postoji. Pokušajte ponovo.\n")
                elif len(letovi2) > 1:
                    print("\nMorate uneti sve podatke o letu.")
                else:
                    let = letovi2[0]
                    break
        else:
            raise Exception ("Nevalidna radnja.")

        broj = karte.sledeci_broj_karte2(sve_karte)
        karta_pomocna = sve_karte[broj]

        datum = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        karta2, sve_karte = karte.kupovina_karte(sve_karte,svi_konkretni_letovi,let["sifra"],karta['putnici'],let['zauzetost'],karta['kupac'],
                                                 datum_prodaje = datetime.strptime(datum,'%Y-%m-%d %H:%M:%S'),prodavac = trenutno_regisrovan)
        sve_karte[karta2["broj_karte"]]["sifra_sedista"] = ""
        sve_karte[karta2["broj_karte"]]["broj_karte"] = broj+1
        sve_karte[broj], sve_karte[broj+1] = karta_pomocna, karta2

        karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
        print("\nUšpesno ste prodali kartu.\n")
        y = input("Da li želite nastaviti sa kupovinom karte za neki povezani let? [da/ne]: ")

        if y.lower() == 'da':
            prodaja_karte(karta2)

def izmena_karte():
    global sve_karte, svi_konkretni_letovi

    y = input("Da li želite videti listu karata? [da/ne]: ")

    if y.lower() == 'da':
        print()
        prikazi_karte(sve_karte)

    broj_karte = eval(input("\nUnesite broj karte za izmenu: "))
    if broj_karte not in sve_karte:
        raise Exception ("Broj karte nije validan.")

    podaci = sve_karte[broj_karte].copy()
    print("Novi podaci karte:\n")
    let =     input("   Šifra konkretnog leta: ")
    sediste = input("   Šifra sedista: ")
    datum =   input("   Datum i vreme polaska (format: 'yyyy-mm-dd hh:mm:ss'): ")

    if let:
        podaci["sifra_konkretnog_leta"] = let
    if sediste:
        podaci["sifra_sedista"] = sediste
    if datum:
        datum = validan_datum(datum,True)
    
    a, b = podaci["sifra_sedista"][:2], podaci["sifra_sedista"][2:]
    podaci["sifra_sedista"] = b + a

    sve_karte = karte.izmena_karte(sve_karte,svi_konkretni_letovi,broj_karte,podaci["sifra_konkretnog_leta"],datum,podaci["sifra_sedista"])
    
    karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
    print("\nUšpesno ste izvrsili izmenu podataka karte.\n")


def prodavac_meni():
    global trenutno_regisrovan, svi_letovi, svi_korisnici, svi_konkretni_letovi, sve_karte
    while 1:
        try:
            prikazi_opcije("prodavac")

            podeli()
            opcija = input("Izaberite opciju: ")
            podeli()

            if opcija == '1':
                prodaja_karte()
            elif opcija == '2':
                izmena_karte()
            elif opcija == '3':
                brisi_kartu(0)
            elif opcija == '4':
                pretrazi_karte()
            elif opcija == '5':
                prijava_na_let(1)
            elif opcija == '6':
                svi_letovi2 = datum_u_div(svi_letovi.copy())
                letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
                prikazi_letove(letovi2)
            elif opcija == '7':
                pretraga_letova(0)
            elif opcija == '8':
                pretraga_letova(1)
            elif opcija == '9':
                top10()
            elif opcija == '10':
                fleksibilni_polasci()
            elif opcija == '11':
                trenutno_regisrovan = None
                karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
                svi_letovi = datum_u_div(svi_letovi)
                letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
                svi_letovi = div_u_datum(svi_letovi)
                konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi)
                korisnici.sacuvaj_korisnike("korisnici.csv",'|',svi_korisnici)
                break
            elif opcija == '12':
                izlaz()
            else:
                raise Exception ("Unesite validnu radnju!")

        except Exception as greska:
            print(greska)


def kreiraj_let():
    print("\n     - KREIRANJE LETA -")

    global svi_letovi, svi_konkretni_letovi, svi_modeli_aviona

    while 1:
        print("\nPodaci o letu:\n"
              "(Datum se unosi u formatu 'yyyy-mm-dd')")
        broj_leta =       input("   Broj leta: ")
        polaziste =       input("   Šifra polazišnog aerodroma: ")
        odrediste =       input("   Šifra odredišnog aerodroma: ")
        datum_pocetka =   input("   Datum pocetka operativnosti (format: 'yyyy-mm-dd'): ")
        datum_kraja   =   input("   Datum kraja operativnosti (format: 'yyyy-mm-dd'): ")
        vreme_poletanja = input("   Vreme poletanja: ")
        vreme_sletanja  = input("   Vreme sletanja: ")
        prevoznik =       input("   Prevoznik: ")
        cena = round(eval(input("   Cena leta: ")),2)
        dani =            input("   Dani leta (u obliku '1 3 5' = pon sre pet): ")

        if datum_pocetka:
            datum_pocetka = validan_datum(datum_pocetka + " 00:00:00",True)
        if datum_kraja:
            datum_kraja = validan_datum(datum_kraja + " 00:00:00",True)

        sletanje_sutra = bool(int(vreme_poletanja[:2]) > int(vreme_sletanja[:2]))
        dani = [eval(i)-1 for i in dani.split(' ')]

        print("   Model aviona:")
        naziv =             input("      Naziv aviona: ")
        broj_redova =  eval(input("      Broj redova: "))
        broj_sedista = eval(input("      Broj sedišta u jednom redu: "))
        
        pozicije_sedista = []
        for broj in range(broj_sedista):
            pozicije_sedista.append(chr(broj+65))

        model = model_aviona.pronadji_model(svi_modeli_aviona,naziv,broj_redova,pozicije_sedista)
        if not model:
            raise Exception ("Model aviona nije pronadjen.")
        svi_letovi = letovi.kreiranje_letova(svi_letovi,broj_leta,polaziste,odrediste,vreme_poletanja,vreme_sletanja,sletanje_sutra,
                                             prevoznik,dani,model,cena,datum_pocetka,datum_kraja)

        svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi,svi_letovi[broj_leta])
        for let in svi_konkretni_letovi.values():
            if let["broj_leta"] == broj_leta:
                letovi.podesi_matricu_zauzetosti(svi_letovi,let)

        svi_letovi[broj_leta]["datum_pocetka_operativnosti"] = svi_letovi[broj_leta]["datum_pocetka_operativnosti"].date()
        svi_letovi[broj_leta]["datum_kraja_operativnosti"] = svi_letovi[broj_leta]["datum_kraja_operativnosti"].date()

        print("\nUspešno ste kreirali novi let.\n")
        break

    svi_letovi = datum_u_div(svi_letovi)
    letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
    svi_letovi = div_u_datum(svi_letovi)
    konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi) 

def izmeni_let():
    global svi_letovi, svi_konkretni_letovi

    print("\n    - IZMENA LETOVA -\n\n")
    y= input("Da li želite da pogledate listu letova? [da/ne]: ")

    if y.lower() == 'da':
        svi_letovi2 = datum_u_div(svi_letovi.copy())
        letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
        prikazi_letove(letovi2)

    broj_leta = input("\nUnesite broj leta za izmenu: ")
    broj_leta.lower()
    if broj_leta not in svi_letovi:
        raise Exception ("Let ne postoji.")
    let = svi_letovi[broj_leta].copy()

    while 1:
        try:
            print("Novi podaci leta:\n")
            print("(Ukoliko neki podatak ne želite da promenite samo pretisnite taster 'Enter')\n")
            polaziste =       input("   Šifra polazišnog aerodroma: ")
            odrediste =       input("   Šifra odredišnog aerodroma: ")
            datum_pocetka =   input("   Datum početka operativnosti: ")
            datum_kraja   =   input("   Datum kraja operativnosti: ")
            vreme_poletanja = input("   Vreme poletanja: ")
            vreme_sletanja  = input("   Vreme sletanja: ")
            prevoznik =       input("   Prevoznik: ")
            cena =            input("   Cena leta: ")
            dani =            input("   Dani leta (u obliku '1 3 5' = pon sre pet): ")

            print("   Model aviona:")
            naziv =             input("      Naziv aviona: ")
            broj_redova =       input("      Broj redova: ")
            broj_sedista =      input("      Broj sedišta u jednom redu: ")

            if polaziste:
                let["sifra_polazisnog_aerodroma"] = polaziste
            if odrediste:
                let["sifra_odredisnog_aerodorma"] = odrediste
            if vreme_poletanja:
                let["vreme_poletanja"] = vreme_poletanja
            if vreme_sletanja:
                let["vreme_sletanja"] = vreme_sletanja
            if prevoznik:
                let["prevoznik"] = prevoznik
            if dani:
                dani = [eval(i)-1 for i in dani.split(' ')]
                let["dani"] = dani
            if cena:
                let["cena"] = round(int(cena),2)
            if datum_pocetka:
                let["datum_pocetka_operativnosti"] = validan_datum(datum_pocetka + " 00:00:00",True)
            if datum_kraja:
                let["datum_kraja_operativnosti"] = validan_datum(datum_kraja + " 00:00:00",True)
            if vreme_poletanja or vreme_sletanja:
                sletanje_sutra = bool(int(let["vreme_poletanja"][:2]) > int(let["vreme_sletanja"][:2]))
            model = let["model"].copy()
            pozicije_sedista = []
            if naziv:
                model["naziv"] = naziv
            if broj_redova:
                model["broj_redova"] = int(broj_redova)
            if broj_sedista:
                for broj in range(int(broj_sedista)):
                    pozicije_sedista.append(chr(broj+65))
                model["pozicije_sedista"] = pozicije_sedista
            let["model"] = model_aviona.pronadji_model(svi_modeli_aviona,model["naziv"],model["broj_redova"],model["pozicije_sedista"])

            svi_letovi = letovi.izmena_letova(svi_letovi,broj_leta,let["sifra_polazisnog_aerodroma"],let["sifra_odredisnog_aerodorma"],let["vreme_poletanja"],let["vreme_sletanja"],
                                              let["sletanje_sutra"],let["prevoznik"],let["dani"],let["model"],let["cena"],let["datum_pocetka_operativnosti"],let["datum_kraja_operativnosti"])
            break
        except Exception as greska:
            print(greska)

    print("Uspesno ste izmenili podatke o letu sa broj leta: '" + broj_leta + "'.")
    svi_letovi = datum_u_div(svi_letovi)
    letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
    svi_letovi = div_u_datum(svi_letovi)

def brisi_kartu(menadzer: bool):
    global sve_karte

    if menadzer:
        #Prikaz karata
        print("Karte za brisanje:\n\n")
        
        karte_za_brisanje = []
        for karta in sve_karte.values():
            if karta["obrisana"]:
                karte_za_brisanje.append(karta)
        
        prikazi_karte(karte_za_brisanje)

        print("\nIzaberite zeljenu radnju:\n"
            "  1. Obrisati sve prikazane karte\n"
            "  2. Obrisati odabrane karte\n"
            "  3. Poništiti brisanje odabranih karata\n")
        opcija = input("Izaberite opciju: ")
        podeli()

        if opcija == '1':
            for broj_karte in karte_za_brisanje:
                sve_karte = karte.brisanje_karte(trenutno_regisrovan,sve_karte,broj_karte)
            print("Sve označene karte su uspešno izbrisane.\n")
        elif opcija == '2':
            while 1:
                broj_karte = input("Unesite broj karte karte koju zelite obrisati: ")
                if broj_karte.lower() == 'x':
                    break
                print("Ukoliko ste završili sa brisanjem karata, unesite 'x'.")
                broj_karte = eval(broj_karte)

                sve_karte = karte.brisanje_karte(trenutno_regisrovan,sve_karte,broj_karte)
            print("Uspešno ste izbrisali odabrane karte.\n")
        elif opcija == '3':
            while 1:
                broj_karte = input("Unesite broj karte karte čije brisanje želite poništiti: ")
                if broj_karte.lower() == 'x':
                    break
                print("Ukoliko ste završili sa unosom karata, unesite 'x'.")
                broj_karte = eval(broj_karte)

                if broj_karte not in sve_karte:
                    raise Exception ("Broj karte nije validan.")

                sve_karte[broj_karte]["obrisana"] = False
            print("Uspešno ste ponistili brisanje izabranih karata.\n")
    else:
        print("Lista karata:\n")
        prikazi_karte(sve_karte)

        broj_karte = eval(input("\nUnesite broj karte za brisanje: "))
        sve_karte = karte.brisanje_karte(trenutno_regisrovan,sve_karte,broj_karte)
        print("\nUspešno ste oznacili kartu za brisanje\n")
    
    karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
        
def izvestavanje():
    global sve_karte

    print("\n    - IZVESTAJI -\n")
    print("Izaberite željeni izvestaj:\n"
          "(Datum se unosi u formatu 'yyyy-mm-dd')\n"
          "  1. Lista prodatih karata za izabrani dan prodaje\n"
          "  2. Lista prodatih karata za izabrani dan polaska\n"
          "  3. Lista prodatih karata za izabrani dan prodaje i izabranog prodavca\n"
          "  4. Ukupan broj i cena prodatih karata za izabrani dan prodaje\n"
          "  5. Ukupan broj i cena prodatih karata za izabrani dan polaska\n"
          "  6. Ukupan broj i cena prodatih karata za izabrani dan prodaje i izabranog prodavca\n"
          "  7. Ukupan broj i cena prodatih karata po prodavcima u prethodnih 30 dana")
        
    podeli()
    opcija = input("Izaberite opciju: ")
    podeli()

    if opcija == '1':
        dan = datetime.strptime(input("Unesite datum prodaje: "),'%Y-%m-%d')
        lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte,dan.date())

        print()
        prikazi_karte(lista)
    elif opcija == '3':
        dan = datetime.strptime(input("Unesite datum prodaje: "),'%Y-%m-%d')
        prodavac = input("Unesite korisničko ime prodavca: ")

        lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte,dan.date(),prodavac)
        print()
        prikazi_karte(lista)
    else:
        global svi_konkretni_letovi, svi_letovi

        if opcija == '2':
            dan = datetime.strptime(input("Unesite datum polaska: "),'%Y-%m-%d')
            lista = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte,svi_konkretni_letovi,dan.date())

            print()
            prikazi_karte(lista)
        elif opcija == '4':
            dan = datetime.strptime(input("Unesite datum prodaje: "),'%Y-%m-%d')
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte,svi_konkretni_letovi,svi_letovi,dan.date())

            print(f"\nUkupan broj prodatih karata: {broj}")
            print(f"Ukupna cena prodatih karata: {cena:.2f}")
        elif opcija == '5':
            dan = datetime.strptime(input("Unesite datum polaska: "),'%Y-%m-%d')
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte,svi_konkretni_letovi,svi_letovi,dan.date())

            print(f"\nUkupan broj prodatih karata: {broj}")
            print(f"Ukupna cena prodatih karata: {cena:.2f}")
        elif opcija == '6':
            dan = datetime.strptime(input("Unesite datum prodaje: "),'%Y-%m-%d')
            prodavac = input("Unesite korisničko ime prodavca: ")
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte,svi_konkretni_letovi,svi_letovi,dan.date(),prodavac)

            print(f"\nUkupan broj prodatih karata: {broj}")
            print(f"Ukupna cena prodatih karata: {cena:.2f}")
        elif opcija == '7':
            prodaje = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte,svi_konkretni_letovi,svi_letovi)
            for prodaja in prodaje.values():
                print("\nProdavac: " + prodaja[2])
                print(f"Ukupan broj prodatih karata: {prodaja[0]}")
                print(f"Ukupna cena prodatih karata: {prodaja[1]:.2f}")
        else:
            raise Exception ("Izabrana opcija ne postoji.\n")
    print()

def pretrazi_karte():
    global sve_karte, svi_letovi, svi_korisnici, svi_konkretni_letovi

    print("Unesite kriterijume za pretragu karata:\n")
    polaziste =       input("   Mesto polaska: ")
    odrediste =       input("   Mesto dolaska: ")
    datum_polaska =   input("   Datum i vreme polaska (format: 'yyyy-mm-dd hh:mm'): ")
    datum_dolaska =   input("   Datum i vreme dolaska (format: 'yyyy-mm-dd hh:mm'): ")
    ime =             input("   Ime putnika: ")
    prezime =         input("   Prezime putnika: ")


    if datum_polaska:
        datum_polaska = datetime.strptime(datum_polaska + ":00",'%Y-%m-%d %H:%M:%S')
    if datum_dolaska:
        datum_dolaska = datetime.strptime(datum_dolaska + ":00",'%Y-%m-%d %H:%M:%S')

    print()
    if ime and prezime:
        print("Korisničko ime putnika:")
        brojac = 1
        korisnicka_imena = []
        for korisnik in svi_korisnici:
            if svi_korisnici[korisnik]["ime"] == ime and svi_korisnici[korisnik]["prezime"] == prezime and svi_korisnici[korisnik]["uloga"] == konstante.ULOGA_KORISNIK:
                print(f"   {brojac}. {korisnik}\n")
                brojac += 1
                korisnicka_imena.append(korisnik)

        if not korisnicka_imena:
            raise Exception ("\nKorisnik ne postoji ili nije registrovan.\n")
        broj = eval(input("Unesite redni broj izabranog korisničkog imena: "))
        
        if broj >= brojac:
            raise Exception ("Nevalidan redni broj.")

        karte2 = karte.pretraga_prodatih_karata(sve_karte,svi_letovi,svi_konkretni_letovi,polaziste,
                                                odrediste,datum_polaska,datum_dolaska,korisnicka_imena[broj-1])
    else:
        karte2 = karte.pretraga_prodatih_karata(sve_karte,svi_letovi,svi_konkretni_letovi,polaziste,
                                                odrediste,datum_polaska,datum_dolaska)

    if not karte2:
        raise Exception ("Nema prodatih karata za unete kriterijume.")
    print()
    prikazi_karte(karte2)


def admin_meni():
    global trenutno_regisrovan, svi_letovi, svi_korisnici, svi_konkretni_letovi, sve_karte
    while 1:
        try:
            prikazi_opcije("menadzer")

            podeli()
            opcija = input("Izaberite opciju: ")
            podeli()

            if opcija == '1':
                pretrazi_karte()
            elif opcija == '2':
                print("\n    - REGISTRACIJA PRODAVACA -")
                registracija(1)
            elif opcija == '3':
                kreiraj_let()
            elif opcija == '4':
                izmeni_let()
            elif opcija == '5':
                print("\n    - BRISANJE KARATA -\n\n")
                brisi_kartu(1)
            elif opcija == '6':
                izvestavanje()
            elif opcija == '7':
                svi_letovi2 = datum_u_div(svi_letovi.copy())
                letovi2 = letovi.pregled_nerealizovanih_letova(svi_letovi2)
                prikazi_letove(letovi2)
            elif opcija == '8':
                pretraga_letova(0)
            elif opcija == '9':
                pretraga_letova(1)
            elif opcija == '10':
                top10()
            elif opcija == '11':
                fleksibilni_polasci()
            elif opcija == '12':
                trenutno_regisrovan = None
                karte.sacuvaj_karte(sve_karte,"karte.csv",'|')
                svi_letovi = datum_u_div(svi_letovi)
                letovi.sacuvaj_letove("letovi.csv",'|',svi_letovi)
                svi_letovi = div_u_datum(svi_letovi)
                konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv",'|',svi_konkretni_letovi)
                korisnici.sacuvaj_korisnike("korisnici.csv",'|',svi_korisnici)
                break
            elif opcija == '13':
                izlaz()
            else:
                raise Exception ("Unesite validnu radnju!")

        except Exception as greska:
            print(greska)

if __name__ == '__main__':
    try:
        svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla("korisnici.csv",'|')
        svi_letovi = letovi.ucitaj_letove_iz_fajla("letovi.csv",'|')
        svi_letovi = div_u_datum(svi_letovi)
        svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let("konkretni_letovi.csv",'|')
        sve_karte = karte.ucitaj_karte_iz_fajla("karte.csv",'|')
        svi_aerodromi = aerodromi.ucitaj_aerodrom("aerodromi.csv",'|')
        svi_modeli_aviona = model_aviona.ucitaj_modele_aviona("avion.csv",'|')
        main()

    except Exception as greska:
        print("Došlo je do greške: " + greska + ".\n")
        svi_aerodromi = None
        svi_konkretni_letovi = None
        svi_korisnici = None
        svi_letovi = None
        sve_karte = None
        izlaz()
