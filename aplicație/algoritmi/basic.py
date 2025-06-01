import numpy as np

litere_mici = np.array((chr(litera) for litera in range(97, 123)))
litere_mari = np.array((chr(litera) for litera in range(65, 91)))

# primeste mesajul (string), numărul de poziții (după care sunt schimbate literele) și acțiunea (criptare sau decriptare)
# mesajul este format strict din litere mari, litere mici sau spatii
def cezar(mesaj, nr_pozitii, actiune):

    if nr_pozitii:
        nr_pozitii %= 26

    if actiune == 'criptare': #criptare

        mesaj_criptat = ''

        for litera in mesaj:
            if litera == ' ':
                litera_criptata = ' '
            elif litera.islower():
                litera_criptata = chr((ord(litera) - 97 + nr_pozitii) % 26 + 97)
            else:
                litera_criptata = chr((ord(litera) - 65 + nr_pozitii) % 26 + 65)
            mesaj_criptat += litera_criptata

        return mesaj_criptat

    elif actiune == 'decriptare': # decriptare

        mesaj_decriptat = ''

        for litera in mesaj:
            if litera == ' ':
                litera_criptata = ' '
            elif litera.islower():
                litera_criptata = chr((ord(litera) - 97 - nr_pozitii) % 26 + 97)
            else:
                litera_criptata = chr((ord(litera) - 65 - nr_pozitii) % 26 + 65)

            mesaj_decriptat += litera_criptata

        return mesaj_decriptat

    else: # spargere

        lista_candidati = []
        for nr_poz in range(1,26): # se incearca toate cele 26 de chei posibile pt spargere
            mesaj_decriptat = ''

            for litera in mesaj:
                if litera == ' ':
                    litera_criptata = ' '
                elif litera.islower():
                    litera_criptata = chr((ord(litera) - 97 - nr_poz) % 26 + 97)
                else:
                    litera_criptata = chr((ord(litera) - 65 - nr_poz) % 26 + 65)

                mesaj_decriptat += litera_criptata

            lista_candidati.append(mesaj_decriptat)

        return lista_candidati


# primeste mesajul (string), numărul de poziții (după care sunt schimbate literele) și acțiunea (criptare sau decriptare)
# mesajul este format strict din litere mari, litere mici sau spatii
def vignere(mesaj, cheie, actiune):

    lung_cheie = len(cheie)

    if actiune == 'criptare':

        index_cheie = 0

        mesaj_criptat = ''

        # se repeta rationamentul urmator pentru fiecare litera din mesaj:
        # litera din mesaj de pe pozitia i e 'shift'-ata cu un numar de pozitii (de ex: 'a' devine 'd')
        # egal cu pozitia in alfabet a literei din cheia de criptare de pe la index-ul i
        # OBS: daca lungimea cheii este mai mica decat cea a mesajului, se efectueaza un wrap-around
        for litera in mesaj:
            if litera == ' ':
                litera_criptata = ' '
            elif litera.islower():
                nr_pozitii = ord(cheie[index_cheie]) - 97
                litera_criptata = chr((ord(litera) - 97 + nr_pozitii) % 26 + 97)
                index_cheie += 1
            else:
                nr_pozitii = ord(cheie[index_cheie]) - 65
                litera_criptata = chr((ord(litera) - 65 + nr_pozitii) % 26 + 65)
                index_cheie += 1
            mesaj_criptat += litera_criptata
            index_cheie %= lung_cheie

        return mesaj_criptat
    else:

        index_cheie = 0

        mesaj_decriptat = ''

        # analog rationamentului de la criptare,
        # doar ca in acest caz se 'shift'-eaza in cealalta directie (de ex: 'd' devine 'a')
        for litera in mesaj:
            if litera == ' ':
                litera_decriptata = ' '
            elif litera.islower():
                nr_pozitii = ord(cheie[index_cheie]) - 97
                litera_decriptata = chr((ord(litera) - 97 - nr_pozitii) % 26 + 97)
                index_cheie += 1
            else:
                nr_pozitii = ord(cheie[index_cheie]) - 65
                litera_decriptata = chr((ord(litera) - 65 - nr_pozitii) % 26 + 65)
                index_cheie += 1
            mesaj_decriptat += litera_decriptata
            index_cheie %= lung_cheie

        return mesaj_decriptat

def main():
    a = cezar('Cr jfriv ifrkr jv drivjkv', None, 'spargere')
    for index, candidat in enumerate(a):
        print(str(index + 1) + '. ' + candidat)
