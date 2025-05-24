import numpy as np

# functie care implementeaza cifrul rivest
# primeste mesajul, cheia de criptare si operatia
# returneaza mesajul criptat/decriptat
# fiind modern, cifrulrivest se bazeaza pe operatii matematice si logice
# si poate cripta mesaje cu orice caracter definit in tabela ascii
def rc4(mesaj, cheie, operatie):

    # rc4 lucreaza pe mesaje de maxim 255 de caractere
    # daca mesajul este de lungime mai mare, il impartim
    # prima parte are 255 de caractere, cealalta are restul caracterelor
    rest_mesaj = None
    if len(mesaj) > 255:
        rest_mesaj = mesaj[255::]
        mesaj = mesaj[:255:]

    lung_cheie = len(cheie)
    lung_mesaj = len(mesaj)

    # consideram permutarea identitate
    permutare = np.array([i for i in range(0, 256)], dtype = int)
    cheie_extinsa = np.zeros((256,), dtype = int)

    # extindem cheia pentru a putea acoperi 256 de caractere
    index_cheie = 0
    for i in range(0, 256):
        cheie_extinsa[i] = ord(cheie[index_cheie])
        index_cheie = (index_cheie + 1) % lung_cheie

    # cheia este folosita pentru a genera un sir de numere pseudo-aleatoare,
    # sirul reprezinta, de fapt, o amestecare a numerelor permutarii identitate
    j = 0
    for i in range (0, 256):
        j = (j + permutare[i] + cheie_extinsa[i % lung_cheie]) % 256
        permutare[i], permutare[j] = permutare[j], permutare[i]

    # se genereaza o cheie curenta, pe baza cheii si a permutarii
    cheie_curenta = np.zeros((lung_mesaj,), dtype = int)
    i = 0; j = 0
    while i < lung_mesaj:
        i = (i + 1) % 256
        j = (j + permutare[i]) % 256
        permutare[i], permutare[j] = permutare[j], permutare[i]
        k = (permutare[i] + permutare[j]) % 256
        cheie_curenta[i - 1] = permutare[k]

    if operatie == 'criptare':

        # mesajul criptat presupune efectuarea operatii de XOR ('si' exclusiv),
        # intre valorile cheii curente si valorile caracterelor din mesaj
        # memorandu-se valorile hexazecimale ale rezultatelor, in mesajul criptat
        mesaj_criptat = ''
        for index, litera in enumerate(mesaj):
            valoare = hex(int(cheie_curenta[index]) ^ ord(litera))[2::]
            valoare = '0' * (2 - len(valoare)) + valoare
            mesaj_criptat += valoare

        rest_mesaj_criptat = ''
        if rest_mesaj: # daca mesajul are mai mult de 255 de caractere
            rest_mesaj_criptat = rc4(rest_mesaj, cheie, operatie) # apelam functia pentru restul mesajului

        return mesaj_criptat + rest_mesaj_criptat # si il adaugam la mesajul final
    else:

        # asemenea operatiei de criptare, decriptarea presupune efectuarea operatii de XOR ('si' exclusiv),
        mesaj_decriptat = ''
        index_mesaj = 0
        index_cheie_curenta = 0
        while index_mesaj < lung_mesaj:
            octet = int(mesaj[index_mesaj:index_mesaj + 2:], 16) # consideram fiecare pereche de valoare hexazecimala ca fiind un octet al mesajului
            mesaj_decriptat += chr(int(cheie_curenta[index_cheie_curenta]) ^ octet) # si efectuam operatia de XOR intre octet si caracterul cheii curente
            index_mesaj += 2
            index_cheie_curenta += 1

        rest_mesaj_decriptat = ''
        if rest_mesaj: # daca mesajul are mai mult de 255 de caractere
            rest_mesaj_decriptat = rc4(rest_mesaj, cheie, operatie) # apelam functia pentru restul mesajului

        return mesaj_decriptat + rest_mesaj_decriptat # si il adaugam la mesajul final

if __name__ == '__main__':
    print(rc4('La soare roata se mareste, la umbra numai carnea creste. Si somn e carnea, se dezumfla, dar fring si umbra iar o umfla.', 'Riga', 'criptare'))

'La soare roata se mareste, la umbra numai carnea creste. Si somn e carnea, se dezumfla, dar fring si umbra iar o umfla.'