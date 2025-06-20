import json


def powitanie():
    print("""
____________________________________________________________________________________________________________

Witaj w systemie rezerwacji biletów w teatrze Scena Nowych Uniesień Sztuki!
Przepraszamy za niedogodności, architekt systemu dopiero się uczy programować.
Oto nasz cennik:
    Miejsce zwykłe: 40 zł
    Miejsce VIP: 60 zł (jeśli z wstępem na spotkanie z aktorami: 120 zł)
    Miejsce dla osób z niepełnosprawnością: 50 zł (jeśli potrzebna pomoc asystenta: 70 zł)
____________________________________________________________________________________________________________

Aby się Zarejestrować, wpisz Z.
Jeśli masz już konto i chcesz:
    - Rezerwować, wpisz R.
    - Wyświetlić swoje rezerwacje i nimi zarządzać, wpisz W.
Aby Usunąć swoje konto, wpisz U.
____________________________________________________________________________________________________________""")

def sztuki_terminy():
    print("""
____________________________________________________________________________________________________________

Aktualnie zapraszamy na sztuki 'Hamlet' i 'Makbet' o stałych godzinach:
    Hamlet - godz. 17:00
    Makbet - godz. 21:00 

w następujących dniach:
    1 - 13 czerwca
    2 - 20 czerwca
____________________________________________________________________________________________________________\n""")

def widok_sali():
        print("""
Oto plan sali:

    AAAAAAAAAA BBBBBBBBBB
    AAAAAAAAAA BBBBBBBBBB
    AAAAAAAAAA BBBBBBBBBB

         OZN OZN OZN
         VIP VIP VIP

            SCENA

Objaśnienia:
    VIP - 20 miejsc VIP
    OZN - 10 miejsc dla osób z niepełnosprawnością
    W sektorach A i B po 20 miejsc na rząd ('jedna litera = 2 miejsca')
    Miejsca w rzędach są numerowane od lewej, patrząc od sceny
____________________________________________________________________________________________________________\n""")

class MiejsceTeatralne:
    def __init__(self, nr, dostepnosc):
        self.nr = nr
        self.dostepnosc = dostepnosc

class MiejsceZwykle(MiejsceTeatralne):
    def __init__(self, nr, dostepnosc):
        super().__init__(nr, dostepnosc)
        self.cena = 40

class MiejsceVIP(MiejsceTeatralne):
    def __init__(self, nr, dostepnosc, czySelfie):
        super().__init__(nr, dostepnosc)
        self.czySelfie = czySelfie
        self.cena = 60
        if czySelfie:
            self.cena = 120

class MiejsceOZN(MiejsceTeatralne):
    def __init__(self, nr, dostepnosc, czyAsystent):
        super().__init__(nr, dostepnosc)
        self.czyAsystent = czyAsystent
        self.cena = 50
        if czyAsystent:
            self.cena = 70

class Klient:
    def __init__(self, imie, nazwisko, mail):
        self.imie = imie
        self.nazwisko = nazwisko
        self.mail = mail

    def dodaj(self):
        with open("klienci.json",encoding="UTF8") as file:
            klienci = json.load(file)
            id = len(klienci) #w takim układzie klientów nie wolno usuwać (musi zostać id)
            klienci.append({"id": id, "imie": self.imie, "nazwisko": self.nazwisko, "mail": self.mail, "rezerwacje":""})
        with open("klienci.json","w",encoding="UTF8") as file:
            json.dump(klienci, file, ensure_ascii=False, indent=4)
        print(f"\nWitaj w systemie, {self.imie} {self.nazwisko}!")

    def usun(self):
        with open("klienci.json",encoding="UTF8") as file:
            klienci = json.load(file)
            for klient in klienci:
                if klient["imie"] == self.imie and klient["nazwisko"] == self.nazwisko and klient["mail"] == self.mail:
                    klient["imie"] = ""
                    klient["nazwisko"] = ""
                    klient["mail"] = ""
                    klient["rezerwacje"] = ""
        with open("klienci.json", "w", encoding="UTF8") as file:
            json.dump(klienci, file, ensure_ascii=False, indent=4)
        print(f"Żegnaj, {self.imie} {self.nazwisko}. Mamy nadzieję, że jeszcze wrócisz!")

    def pokazWszystkich(self):
        with open("klienci.json",encoding="UTF8") as file:
            klienci = json.load(file)
            print("Oto lista wszystkich klientów (pomijam usuniętych):")
            for klient in klienci:
                if klient["imie"] != "":
                    print(klient)

    def pokazPoMailu(self):
        with open("klienci.json",encoding="UTF8") as file:
            klienci = json.load(file)
            for klient in klienci:
                if klient["mail"]==self.mail:
                    print(klient)

    #dwie ostatnie metody są zasadniczo zbędne, ale żal je usuwać 8)

class Teatr:
    def __init__(self, sztuka, termin, id_klienta):
        self.sztuka = sztuka
        self.termin = termin
        self.id_klienta = id_klienta

    def pokazSektor(self):
        powtorz_sektor = "T"
        while powtorz_sektor == "T" or powtorz_sektor == "t":
            with open(f"{self.sztuka}_{self.termin}.json",encoding="UTF8") as file:
                sektor=input("Podaj sektor, który chcesz obejrzeć (wpisz dużą literę A lub B, albo skrót OZN lub VIP): ")
                miejsca = json.load(file)
                print("\n\nOto lista dostępnych miejsc w wybranym przez Ciebie sektorze:\n")
                for miejsce in miejsca:
                    if miejsce["sektor"] == sektor and miejsce["dostepnosc"] == "wolne":
                        print(f"{miejsce["sektor"]}, rząd: {miejsce["rzad"]}, numer: {miejsce["nr"]}")
            powtorz_sektor=input("Jeśli chcesz obejrzeć inny sektor, wpisz literę T. Jeśli przejść do rezerwacji, dowolny znak. Zatwierdź enterem: ")

    def rezerwuj(self):

        # print(f"Rezerwujemy dla klienta o numerze: {self.id_klienta}.")
        sektor=input("Podaj, w którym sektorze chcesz rezerwować (wpisz dużą literę A lub B, albo skrót OZN lub VIP): ")
        ile = int(input("Podaj, ile miejsc chcesz zarezerwować: "))

        if sektor == "A" or sektor == "B":

            koszt=[]
            for i in range(ile):
                nr = int(input(f"Podaj nr miejsca {i+1}: "))
                m=(MiejsceZwykle(nr,"zajete"))

                with open(f"{self.sztuka}_{self.termin}.json",encoding="UTF8") as file:
                    sloty = json.load(file)
                    for slot in sloty:
                        if slot["nr"]==m.nr:
                            slot["dostepnosc"]=m.dostepnosc
                with open(f"{self.sztuka}_{self.termin}.json","w",encoding="UTF8") as file:
                    json.dump(sloty, file, ensure_ascii=False, indent=4)


                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                    rezerwacje = json.load(file)
                    id_klienta_str = str(self.id_klienta)
                    if id_klienta_str not in rezerwacje:
                        rezerwacje[id_klienta_str] = []

                rezerwacja = {
                    "sektor": sektor,
                    "nr": m.nr,
                    "dostepnosc": m.dostepnosc
                }

                rezerwacje[id_klienta_str].append(rezerwacja)

                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                    json.dump(rezerwacje, file, ensure_ascii=False, indent=4)

                koszt.append(m.cena)
            suma = 0
            for pozycja in koszt:
                suma+=pozycja
            print(f"Zarezerwowano biletów: {ile} za {suma} zł łącznie.")

        if sektor == "OZN":

            koszt = []
            for i in range(ile):
                nr = int(input(f"Podaj nr miejsca {i+1}: "))
                asysta=input("Jeśli potrzebujesz wsparcia asystenta (dodatkowy koszt 20 zł, łączny 70 zł), wpisz T. Jeśli nie, dowolny znak. Zatwierdź enterem: ")
                if asysta == "T" or asysta == "t":
                    asysta_bool = True
                else:
                    asysta_bool = False
                m = (MiejsceOZN(nr, "zajete",asysta_bool))

                with open(f"{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                    sloty = json.load(file)
                    for slot in sloty:
                        if slot["nr"] == m.nr:
                            slot["dostepnosc"] = m.dostepnosc
                            slot["czyAsystent"] = m.czyAsystent
                with open(f"{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                    json.dump(sloty, file, ensure_ascii=False, indent=4)

                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                    rezerwacje = json.load(file)
                    id_klienta_str = str(self.id_klienta)
                    if id_klienta_str not in rezerwacje:
                        rezerwacje[id_klienta_str] = []

                rezerwacja = {
                    "sektor": sektor,
                    "nr": m.nr,
                    "dostepnosc": m.dostepnosc,
                    "czyAsystent": m.czyAsystent
                }

                rezerwacje[id_klienta_str].append(rezerwacja)

                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                    json.dump(rezerwacje, file, ensure_ascii=False, indent=4)

                koszt.append(m.cena)
            suma = 0
            for pozycja in koszt:
                suma += pozycja
            print(f"Zarezerwowano biletów: {ile} za {suma} zł łącznie.")

        if sektor == "VIP":

            koszt = []
            for i in range(ile):
                nr = int(input(f"Podaj nr miejsca {i+1}: "))
                selfie=input("Jeśli chcesz dokupić możliwość wejścia na spotkanie z aktorami (dodatkowy koszt 60 zł, łączny 120 zł), wpisz T. Jeśli nie, dowolny znak. Zatwierdź enterem: ")
                if selfie == "T" or selfie == "t":
                    selfie_bool = True
                else:
                    selfie_bool = False
                m = (MiejsceVIP(nr, "zajete",selfie_bool))

                with open(f"{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                    sloty = json.load(file)
                    for slot in sloty:
                        if slot["nr"] == m.nr:
                            slot["dostepnosc"] = m.dostepnosc
                            slot["czySelfie"] = m.czySelfie
                with open(f"{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                    json.dump(sloty, file, ensure_ascii=False, indent=4)

                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                    rezerwacje = json.load(file)
                    id_klienta_str = str(self.id_klienta)
                    if id_klienta_str not in rezerwacje:
                        rezerwacje[id_klienta_str] = []

                rezerwacja = {
                    "sektor": sektor,
                    "nr": m.nr,
                    "dostepnosc": m.dostepnosc,
                    "czySelfie": m.czySelfie
                }

                rezerwacje[id_klienta_str].append(rezerwacja)

                with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                    json.dump(rezerwacje, file, ensure_ascii=False, indent=4)

                koszt.append(m.cena)
            suma = 0
            for pozycja in koszt:
                suma += pozycja
            print(f"Zarezerwowano biletów: {ile} za {suma} zł łącznie.")

    def wyswietl(self):

        with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
            rezerwacje = json.load(file)
            rezerwacje_klienta = rezerwacje.get(f"{self.id_klienta}",[])
            for r in rezerwacje_klienta:
                if r["sektor"] == "VIP":
                    cena = 60
                    if r["czySelfie"]:
                        cena = 120
                if r["sektor"] == "OZN":
                    cena = 50
                    if r["czyAsystent"]:
                        cena = 70
                if r["sektor"] == "A" or r["sektor"] == "B":
                    cena = 40

                print(f"Sektor: {r["sektor"]}, nr {r["nr"]}, koszt: {cena} zł")

    def anuluj(self):
        ile = int(input("Podaj, ile miejsc chcesz anulować: "))

        kasacja = []
        for i in range(ile):
            nr = int(input(f"Podaj nr miejsca {i + 1}. przeznaczonego do anulowania: "))
            m = MiejsceTeatralne(nr, "wolne")

            with open(f"{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                sloty = json.load(file)
                for slot in sloty:
                    if slot["nr"] == m.nr:
                        slot["dostepnosc"] = m.dostepnosc
            with open(f"{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                json.dump(sloty, file, ensure_ascii=False, indent=4)

            with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", encoding="UTF8") as file:
                rezerwacje = json.load(file)
                id_klienta_str = str(self.id_klienta)

            rezerwacje[id_klienta_str] = [r for r in rezerwacje[id_klienta_str] if not (r["nr"] == m.nr)]

            with open(f"rezerwacje_{self.sztuka}_{self.termin}.json", "w", encoding="UTF8") as file:
                json.dump(rezerwacje, file, ensure_ascii=False, indent=4)

            kasacja.append(m.nr)

        print(f"Anulowano rezerwację miejsc o numerach: {kasacja}")

powitanie()
decyzja = input("Co robimy? Wpisz jedną literę z powyższych i wciśnij enter: ")

if decyzja == "U" or decyzja == "u":
    print("\nWybrano opcję usunięcia konta. Aby rezerwować, konieczne będzie za chwilę utworzenie nowego konta.")
    k=Klient(input("Podaj imię do usunięcia: "),input("Podaj nazwisko do usunięcia: "),input("Podaj adres e-mail do usunięcia: "))
    k.usun()
    decyzja="Z"

if decyzja == "Z" or decyzja == "z":
    print("\nZarejestruj nowe konto. Po rejestracji przeniesiemy Cię do panelu rezerwowania.")
    k=Klient(input("Podaj imię: "),input("Podaj nazwisko: "),input("Podaj adres e-mail: "))
    k.dodaj()
    decyzja="R"

while decyzja == "W" or decyzja == "w":

    mail=input("Podaj adres e-mail przypisany do konta, dla którego rezerwacje chcesz wyświetlić: ")

    with open("klienci.json", encoding="UTF8") as file:
        klienci = json.load(file)
        for klient in klienci:
            if klient["mail"] == mail:
                imie = klient["imie"]
                nazwisko = klient["nazwisko"]
                id_klienta = klient["id"]

    k = Klient(imie, nazwisko, mail)
    print(f"Sprawdźmy Twoje zamówienia, {k.imie} {k.nazwisko}!")
    # print(f"Twój nr w systemie to: {id_klienta}") #tak dla sprawdzenia, czy wziął id jak należy
    decyzja2 = "T"
    while decyzja2 == "T" or decyzja2 == "t":
        sztuki_terminy()
        widok_sali()
        print("Aby wyświetlić swoje rezerwacje: ")
        t = Teatr(input("Podaj nazwę sztuki (dużą literą): "),int(input("Wybierz termin, podając cyfrę (nie dzień): ")), id_klienta)

        t.wyswietl()
        decyzja3=input("Czy chcesz anulować jedną lub więcej z powyższych rezerwacji? Jeśli tak, wpisz literę T. Jeśli nie, dowolny inny znak. Zatwierdź enterem: ")
        if decyzja3 == "T" or decyzja3 == "t":
            t.anuluj()

        decyzja2 = input(f"\nCzy chcesz zarządzać rezerwacjami na inny termin/sztukę z konta {k.imie} {k.nazwisko}? Jeśli tak, wpisz literę T. Jeśli nie, dowolny inny znak. Zatwierdź enterem: ")

    decyzja=input("\nCzy chcesz zarządzać rezerwacjami dla innego konta? \nJeśli tak, wpisz literę W. Jeśli nie, dowolny inny znak. Zatwierdź enterem: ")

while decyzja == "R" or decyzja == "r":

    mail=input("Podaj adres e-mail przypisany do Twojego konta: ")

    with open("klienci.json", encoding="UTF8") as file:
        klienci = json.load(file)
        for klient in klienci:
            if klient["mail"] == mail:
                imie = klient["imie"]
                nazwisko = klient["nazwisko"]
                id_klienta = klient["id"]

    k=Klient(imie,nazwisko,mail)
    print(f"Zapraszamy do rezerwowania, {k.imie} {k.nazwisko}!")
    # print(f"Twój nr w systemie to: {id_klienta}") #tak dla sprawdzenia, czy wziął id jak należy
    decyzja2="T"
    while decyzja2 == "T" or decyzja2 == "t":
        sztuki_terminy()
        t=Teatr(input("Podaj nazwę sztuki (dużą literą): "), int(input("Wybierz termin, podając cyfrę (nie dzień): ")),id_klienta)
        widok_sali()
        t.pokazSektor()
        t.rezerwuj()

        decyzja2=input(f"\nCzy chcesz rezerwować ponownie dla konta {k.imie} {k.nazwisko}? Jeśli tak, wpisz literę T. Jeśli nie, dowolny inny znak. Zatwierdź enterem: ")

    decyzja=input("\nCzy chcesz rezerwować ponownie na innym koncie? \nJeśli tak, wpisz literę R. Jeśli nie, dowolny inny znak. Zatwierdź enterem: ")


print("Dziękujemy za skorzystanie z systemu. Do zobaczenia ponownie!")




