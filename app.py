import json
from operator import truediv


def powitanie():
    print("""
____________________________________________________________________________________________________________

Witaj w systemie rezerwacji biletów w teatrze Scena Nowych Uniesień Sztuki!
Oto nasz cennik:
    Miejsce zwykłe: 40 zł
    Miejsce VIP: 60 zł (jeśli z wstępem na spotkanie z aktorami: 120 zł)
    Miejsce dla osób z niepełnosprawnością: 50 zł (jeśli potrzebna pomoc asystenta: 70 zł)""")

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
            klienci.append({"id": id, "imie": self.imie, "nazwisko": self.nazwisko, "mail": self.mail})
        with open("klienci.json","w",encoding="UTF8") as file:
            json.dump(klienci, file, ensure_ascii=False, indent=4)
        print(f"Witaj w systemie, {self.imie} {self.nazwisko}!")

    def usun(self):
        with open("klienci.json",encoding="UTF8") as file:
            klienci = json.load(file)
            for klient in klienci:
                if klient["imie"] == self.imie and klient["nazwisko"] == self.nazwisko and klient["mail"] == self.mail:
                    klient["imie"] = ""
                    klient["nazwisko"] = ""
                    klient["mail"] = ""
        with open("klienci.json", "w", encoding="UTF8") as file:
            json.dump(klienci, file, ensure_ascii=False, indent=4)

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

    def pokazRezerwacjeKlienta(self):
        pass
        # tu skorzystamy z pliku rezerwacje.json gdzie będą klienci i ich wszystkie rezerwacje (pamiętaj żeby uwzględniać rezerwacje z różnych sztuk i terminów!)

class Teatr:
    def __init__(self, sztuka, termin):
        self.sztuka = sztuka
        self.termin = termin


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
        #powinno odhaczać (wolne/zajęte) miejsce w pliku (np. Hamlet_1.json) zawierającym stan sali na Hamleta (np. 13 czerwca)

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
                koszt.append(m.cena)
            suma = 0
            for pozycja in koszt:
                suma += pozycja
            print(f"Zarezerwowano biletów: {ile} za {suma} zł łącznie.")

        """teraz musimy 
        ZAŻĄDAĆ REJESTRACJI W KTÓRYMŚ MOMENCIE
        dołożyć anulowanie czyli chyba po prostu odwrócenie powyższego
        no i na końcu to połączenie klientów z rezerwacjami :v"""



        # with open(f"{self.sztuka}_{self.termin}.json",encoding="UTF8") as file:
            # rezerwacje = input("Podaj, po przecinku i bez spacji, numery miejsc które chcesz zarezerwować: ")
            # lista_int = [int(slot) for slot in rezerwacje.split(",")]
            # zarezerwowane = [MiejsceVIP(lista_int[x],"zajete",True) for x in range(len(lista_int))]

            # for x in range(len(lista_int)-1):
            #     r[x]=MiejsceZwykle(x,"zajete")
            # print(r)
        #     miejsca = json.load(file)
        #     for miejsce in rezerwacje:
        #         if klient["imie"] == self.imie and klient["nazwisko"] == self.nazwisko and klient["mail"] == self.mail:
        #             klient["imie"] = ""
        #             klient["nazwisko"] = ""
        #             klient["mail"] = ""
        #
        # with open(f"{self.sztuka}_{self.termin}.json",encoding="UTF8") as file:
        #     json.dump(klienci, file, ensure_ascii=False, indent=4)

    def anuluj(self):
        pass

powitanie()
powtorz = "T"
while powtorz == "T" or powtorz=="t":

    sztuki_terminy()
    t=Teatr(input("Podaj nazwę sztuki (dużą literą): "), int(input("Wybierz termin, podając cyfrę (nie dzień): ")))
    widok_sali()
    t.pokazSektor()
    #no i dobra, tera rezerwujemy metodą(?) Teatr.rezerwuj, ale wykorzystując klasy Miejsce - ciekawe jak XD
    #   k=Klient(input("Podaj imię: "), input("Podaj nazwisko: "), input("Podaj adres e-mail: "))
    #   k.dodaj()
    t.rezerwuj()


    powtorz=input("\nCzy chcesz rezerwować ponownie? \nJeśli tak, wpisz literę T. Jeśli nie, dowolny znak. Zatwierdź enterem: ")





#

#   k2.pokazPoMailu()
#   k2.usun()


# Klient.dodaj((),"Elżbieta","Bączek","baczek@onet.pl")

# Klient.pokazPoMailu()

# Klient.pokazWszystkich(())




# m1=MiejsceOZN("OZN", 1, "wolne", True)

# m2=MiejsceVIP("VIP", 2, "zajęte", False)

# m3=MiejsceZwykle("A", 3, "wolne")

# [
#     {
#         "id": 0,
#         "imie": "Jan",
#         "nazwisko": "Kowalski",
#         "mail": "kowal@wp.pl"
#     }
#
# ]
#

print("Dziękujemy za skorzystanie z systemu. Do zobaczenia ponownie!") #podnieś potem gdzieś wyżej