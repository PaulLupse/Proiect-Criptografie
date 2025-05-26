import numpy as np
import sympy as sp

# functie care implementeaza cifrul playfair
# primeste mesajul, cheia de criptare si operatia
# returneaza mesajul criptat/decriptat
def playfair(mesaj, cheie, operatie):

    cheie = cheie.lower().replace(' ', '')
    lung_cheie = len(cheie)

    cheie.translate({106 : 105}) # toate caracterele 'j' sunt inlocuite cu caractere 'i' (datorita limitarii algoritmului)

    mesaj = mesaj.lower().replace(' ', '')

    mesaj.translate({106 : 105}) # toate caracterele 'j' sunt inlocuite cu caractere 'i' (datorita limitarii algoritmului)

    # alfabetul se construieste astfel: se adauga fiecare caracter din cheie, o singura data
    # (daca un caracter este intalnit dinnou, acesta e ignorat)
    alfabet = ''
    multime_litere = set()
    for i in range(0, lung_cheie):
        if cheie[i] not in multime_litere:
            multime_litere.add(cheie[i])
            alfabet += cheie[i]

    # apoi se adauga restul caracterelor din alfabet
    for i in range(0, 26):
        if chr(i + 97) not in multime_litere and chr(i + 97) != 'j':
            multime_litere.add(chr(i + 97))
            alfabet += chr(i + 97)

    # caracterele sunt asezate intr-o matrice patratica de marime 5
    matrice_criptare = np.zeros((5, 5), dtype = str)

    index_alfabet = 0
    for i in range(0, 5):
        for j in range(0, 5):
            matrice_criptare[i][j] = alfabet[index_alfabet]
            index_alfabet += 1

    # fiecarui caracter ii este atribuit un cod (linia si coloana pe care se afla)
    cod_caracter = {}
    for k in range(0, 25):
        cod_caracter[alfabet[k]] = (k // 5, k % 5)

    if operatie == 'criptare':

        # mesajul e impartit in perechi de caractere
        digrame = []
        i = 0
        while i < len(mesaj) - 1:
            if mesaj[i] == mesaj[i + 1]: # daca o pereche contine caractere similare,
                mesaj = mesaj[:i + 1:] + 'q' + mesaj[i+1::] # este adaugat caracterul 'q' (filler) intre cele doua (in string),
                                                            # iar al doilea caracter din pereche va fii considerat la urmatoarea pereche
                                                            # in timp ce perechea curenta va avea al doilea caracter 'q'
                
            digrame.append((mesaj[i], mesaj[i + 1]))
            i += 2 
        
        # daca mesajul este de lungime impara, se adauga litera 'q' (filler)
        if len(mesaj) % 2 == 1:
            digrame.append((mesaj[len(mesaj) - 1], 'q'))

        mesaj_criptat = ''
        for litera1, litera2 in digrame:
            
            # pentru fiecare pereche de litere, consideram codul acesteia
            cod_litera_1 = cod_caracter[litera1]
            cod_litera_2 = cod_caracter[litera2]

            # daca liniile sunt aceleasi
            if cod_litera_1[0] == cod_litera_2[0]:

                # are loc o shiftare spre dreapta in matrice
                # cu wrap-around in caz ca se atinge marginea din dreapta
                mesaj_criptat += matrice_criptare[cod_litera_1[0]][(cod_litera_1[1] + 1) % 5]
                mesaj_criptat += matrice_criptare[cod_litera_2[0]][(cod_litera_2[1] + 1) % 5]

            # daca coloanele sunt aceleasi
            elif cod_litera_1[1] == cod_litera_2[1]:

                # are loc o shiftare in jos in matrice
                # cu wrap-around in caz ca se atinge marginea de jos
                mesaj_criptat += matrice_criptare[(cod_litera_1[0] + 1) % 5][cod_litera_1[1]]
                mesaj_criptat += matrice_criptare[(cod_litera_2[0] + 1) % 5][cod_litera_2[1]]

            # daca liniile si coloanele sunt diferite (codurile literelor sunt colturi opuse ale unui dreptunghi)
            else:

                # se face schimb de coloane
                mesaj_criptat += matrice_criptare[cod_litera_1[0]][cod_litera_2[1]]
                mesaj_criptat += matrice_criptare[cod_litera_2[0]][cod_litera_1[1]]

        return mesaj_criptat

    else:

        lung_mesaj = len(mesaj)

        digrame = []
        i = 0
        while i < lung_mesaj - 1:
            digrame.append((mesaj[i], mesaj[i + 1]))
            i += 2

        mesaj_decriptat = ''
        for litera1, litera2 in digrame:

            # pentru fiecare pereche de litere, consideram codul acesteia
            cod_litera_1 = cod_caracter[litera1]
            cod_litera_2 = cod_caracter[litera2]

            # daca liniile sunt aceleasi
            if cod_litera_1[0] == cod_litera_2[0]:

                # are loc o shiftare spre stanga in matrice
                # cu wrap-around in caz ca se atinge marginea din stanga
                neg1 = (cod_litera_1[1] == 0)
                neg2 = (cod_litera_2[1] == 0)
                mesaj_decriptat += matrice_criptare[cod_litera_1[0]][(cod_litera_1[1] - 1) + 5 * neg1]
                mesaj_decriptat += matrice_criptare[cod_litera_2[0]][(cod_litera_2[1] - 1) + 5 * neg2]

            # daca coloanele sunt aceleasi
            elif cod_litera_1[1] == cod_litera_2[1]:

                # are loc o shiftare spre dreapta in matrice
                # cu wrap-around in caz ca se atinge marginea din dreapta
                neg1 = (cod_litera_1[0] == 0)
                neg2 = (cod_litera_2[0] == 0)
                mesaj_decriptat += matrice_criptare[(cod_litera_1[0] - 1) + 5 * neg1][cod_litera_1[1]]
                mesaj_decriptat += matrice_criptare[(cod_litera_2[0] - 1) + 5 * neg2][cod_litera_2[1]]

            else:

                # se face schimb de coloane
                mesaj_decriptat += matrice_criptare[cod_litera_1[0]][cod_litera_2[1]]
                mesaj_decriptat += matrice_criptare[cod_litera_2[0]][cod_litera_1[1]]

        # daca ultimul caracter este 'q', il vom considera filler si il eliminam
        if mesaj_decriptat[-1] == 'q':
                mesaj_decriptat = mesaj_decriptat[:-1:]

        l = len(mesaj_decriptat)
        for i in range(l - 1, 1, -1):
            # daca detectam caractere 'q' intre doua caractere asemenea, le consideram filler si le eliminam
            if mesaj_decriptat[i] == mesaj_decriptat[i - 2] and mesaj_decriptat[i - 1] == 'q':
                mesaj_decriptat = mesaj_decriptat[:i - 1:] + mesaj_decriptat[i::]

        return mesaj_decriptat


# functie care implementeaza cifrul hill
# primeste mesajul, cheia de criptare si operatia
# returneaza mesajul criptat/decriptat
def hill(mesaj, cheie, operatie):

    mesaj = mesaj.lower().replace(' ', '') # eliminarea spatiilor este necesara
    lung_mesaj = len(mesaj)

    cheie = cheie.lower()
    sqrt_lung_cheie = int(len(cheie) ** (1/2))

    while len(mesaj) % sqrt_lung_cheie != 0: # daca mesajul nu este de lungime divizibila cu 2 sau 3
        mesaj += 'q'   # adaugam un caracter filler

    # construim matricea de criptare, care are ca elemente pozitiile din alfabet ale caracterelor cheii
    matrice_cheie = np.zeros((sqrt_lung_cheie, sqrt_lung_cheie), dtype = int)
    index_cheie = 0
    for i in range(0, sqrt_lung_cheie):
        for j in range(0, sqrt_lung_cheie):
            matrice_cheie[i][j] = ord(cheie[index_cheie]) - 97
            index_cheie += 1

    if operatie == 'criptare':
        mesaj_criptat = ''
        index_mesaj = 0
        while index_mesaj < lung_mesaj:

            # impartim mesajul in secvente de 2 sau 3 caractere
            secv = mesaj[index_mesaj:index_mesaj + sqrt_lung_cheie:]

            # consideram pozitiile acestora din alfabet, si le adaugam intr-o matrice vector...
            secv_vectorial = np.zeros((sqrt_lung_cheie,), dtype = int)
            for index, litera in enumerate(secv):
                secv_vectorial[index] = ord(litera) - 97

            # ... pe care o inmultim cu matricea cheie, modulo 26
            rezultat = np.matmul(matrice_cheie, secv_vectorial)

            # elementele din rezultat reprezinta pozitii ale unor litere din alfabet,
            # adaugam aceste litere la mesajul criptat
            mesaj_criptat += ''.join([chr(nr % 26 + 97) for nr in rezultat])
            mesaj_criptat += ' '

            index_mesaj += sqrt_lung_cheie

        return mesaj_criptat

    # operatia de criptare e similara,
    # singura diferenta fiind faptul ca inmultim matricile vector cu inversa matricei cheie
    else:
        print(matrice_cheie)
        # inversa matricei este calculata modulo 26
        inversa_matrice_cheie = np.array(sp.Matrix(matrice_cheie).inv_mod(26))

        mesaj_decriptat = ''
        index_mesaj = 0
        while index_mesaj < lung_mesaj:

            # impartim mesajul in secvente de 2 sau 3 caractere
            secv = mesaj[index_mesaj:index_mesaj + sqrt_lung_cheie:]

            # consideram pozitiile acestora din alfabet, si le adaugam intr-o matrice vector...
            secv_vectorial = np.zeros((sqrt_lung_cheie,), dtype=int)
            for index, litera in enumerate(secv):
                secv_vectorial[index] = ord(litera) - 97

            # ... pe care o inmultim cu matricea cheie, modulo 26
            rezultat = np.matmul(inversa_matrice_cheie, secv_vectorial)

            # elementele din rezultat reprezinta pozitii ale unor litere din alfabet,
            # adaugam aceste litere la mesajul criptat
            mesaj_decriptat += ''.join([chr(nr % 26 + 97) for nr in rezultat])

            index_mesaj += sqrt_lung_cheie

        # caracterele z de la sfarsit le consideram filler
        while ((mesaj_decriptat[-1] == 'q')
               and ((len(mesaj_decriptat) - 1) % sqrt_lung_cheie > 0)):
            mesaj_decriptat = mesaj_decriptat[:-1:]

        return mesaj_decriptat

if __name__ == '__main__':
    a = hill('gp', 'AHGJ', 'decriptare')
    print(a)
