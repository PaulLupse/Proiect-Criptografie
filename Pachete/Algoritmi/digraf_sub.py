import numpy as np
import sympy as sp

def __sterge_spatii(mesaj):
    i = 0
    while i < len(mesaj):
        if mesaj[i] == ' ':
            mesaj = mesaj[0:i:] + mesaj[i + 1::]
        else:
            i += 1
    return mesaj

def playfair(mesaj, cheie, operatie):

    cheie = __sterge_spatii(cheie.lower())
    lung_cheie = len(cheie)

    cheie.translate({106 : 105})

    mesaj = __sterge_spatii(mesaj.lower())

    mesaj.translate({106 : 105})

    alfabet = ''
    multime_litere = set()
    for i in range(0, lung_cheie):
        if cheie[i] not in multime_litere:
            multime_litere.add(cheie[i])
            alfabet += cheie[i]

    for i in range(0, 26):
        if chr(i + 97) not in multime_litere and chr(i + 97) != 'j':
            multime_litere.add(chr(i + 97))
            alfabet += chr(i + 97)

    matrice_criptare = np.zeros((5, 5), dtype = str)

    index_alfabet = 0
    for i in range(0, 5):
        for j in range(0, 5):
            matrice_criptare[i][j] = alfabet[index_alfabet]
            index_alfabet += 1

    cod_caracter = {}
    for k in range(0, 25):
        cod_caracter[alfabet[k]] = (k // 5, k % 5)

    print(matrice_criptare)

    if operatie == 'criptare':

        digrame = []
        i = 0
        while i < len(mesaj) - 1:
            if mesaj[i] == mesaj[i + 1]:
                mesaj = mesaj[:i + 1:] + 'q' + mesaj[i+1::]
            digrame.append((mesaj[i], mesaj[i + 1]))
            i += 2

        if len(mesaj) % 2 == 1:
            digrame.append((mesaj[len(mesaj) - 1], 'q'))

        mesaj_criptat = ''
        for litera1, litera2 in digrame:
            if cod_caracter[litera1][0] == cod_caracter[litera2][0]:

                mesaj_criptat += matrice_criptare[cod_caracter[litera1][0]][(cod_caracter[litera1][1] + 1) % 5]
                mesaj_criptat += matrice_criptare[cod_caracter[litera2][0]][(cod_caracter[litera2][1] + 1) % 5]

            elif cod_caracter[litera1][1] == cod_caracter[litera2][1]:

                mesaj_criptat += matrice_criptare[(cod_caracter[litera1][0] + 1) % 5][cod_caracter[litera1][1]]
                mesaj_criptat += matrice_criptare[(cod_caracter[litera2][0] + 1) % 5][cod_caracter[litera2][1]]
            
            else:
                
                mesaj_criptat += matrice_criptare[cod_caracter[litera1][0]][cod_caracter[litera2][1]]
                mesaj_criptat += matrice_criptare[cod_caracter[litera2][0]][cod_caracter[litera1][1]]

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
            if cod_caracter[litera1][0] == cod_caracter[litera2][0]:

                neg1 = (cod_caracter[litera1][1] == 0)
                neg2 = (cod_caracter[litera2][1] == 0)
                mesaj_decriptat += matrice_criptare[cod_caracter[litera1][0]][(cod_caracter[litera1][1] - 1) + 5 * neg1]
                mesaj_decriptat += matrice_criptare[cod_caracter[litera2][0]][(cod_caracter[litera2][1] - 1) + 5 * neg2]

            elif cod_caracter[litera1][1] == cod_caracter[litera2][1]:

                neg1 = (cod_caracter[litera1][0] == 0)
                neg2 = (cod_caracter[litera2][0] == 0)
                mesaj_decriptat += matrice_criptare[(cod_caracter[litera1][0] - 1) + 5 * neg1][cod_caracter[litera1][1]]
                mesaj_decriptat += matrice_criptare[(cod_caracter[litera2][0] - 1) + 5 * neg2][cod_caracter[litera2][1]]

            else:

                mesaj_decriptat += matrice_criptare[cod_caracter[litera1][0]][cod_caracter[litera2][1]]
                mesaj_decriptat += matrice_criptare[cod_caracter[litera2][0]][cod_caracter[litera1][1]]

        if mesaj_decriptat[-1] == 'q':
                mesaj_decriptat = mesaj_decriptat[:-1:]

        l = len(mesaj_decriptat)
        for i in range(l - 1, 1, -1):
            if mesaj_decriptat[i] == mesaj_decriptat[i - 2] and mesaj_decriptat[i - 1] == 'q':
                mesaj_decriptat = mesaj_decriptat[:i - 1:] + mesaj_decriptat[i::]

        return mesaj_decriptat

def hill(mesaj, cheie, operatie):

    mesaj = __sterge_spatii(mesaj.lower())
    lung_mesaj = len(mesaj)

    cheie = cheie.lower()
    sqrt_lung_cheie = int(len(cheie) ** (1/2))

    while len(mesaj) % sqrt_lung_cheie != 0:
        mesaj += 'z'

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

            secv = mesaj[index_mesaj:index_mesaj + sqrt_lung_cheie:]
            secv_vectorial = np.zeros((sqrt_lung_cheie,), dtype = int)
            for index, litera in enumerate(secv):
                secv_vectorial[index] = ord(litera) - 97

            rezultat = np.matmul(matrice_cheie, secv_vectorial)

            mesaj_criptat += ''.join([chr(nr % 26 + 97) for nr in rezultat])
            mesaj_criptat += ' '

            index_mesaj += sqrt_lung_cheie

        return mesaj_criptat

    else:

        inversa_matrice_cheie = np.array(sp.Matrix(matrice_cheie).inv_mod(26))


        mesaj_decriptat = ''
        index_mesaj = 0
        while index_mesaj < lung_mesaj:

            secv = mesaj[index_mesaj:index_mesaj + sqrt_lung_cheie:]
            secv_vectorial = np.zeros((sqrt_lung_cheie,), dtype=int)
            for index, litera in enumerate(secv):
                secv_vectorial[index] = ord(litera) - 97

            rezultat = np.matmul(inversa_matrice_cheie, secv_vectorial)

            mesaj_decriptat += ''.join([chr(nr % 26 + 97) for nr in rezultat])

            index_mesaj += sqrt_lung_cheie

        return mesaj_decriptat

if __name__ == '__main__':
    a = hill('glw xop ewh osl ick wal wgp ifa jes usb ccw doj szq iaz wgp', 'GYBNQKURP', 'decriptare')
    print(a)
