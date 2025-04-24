import numpy as np
import math
from functools import cmp_to_key

def sterge_spatii(mesaj):
    i = 0
    while i < len(mesaj):
        if mesaj[i] == ' ':
            mesaj = mesaj[0:i:] + mesaj[i + 1::]
        else:
            i += 1
    return mesaj

def polybius(mesaj, alfabet, operatie):

    mesaj = mesaj.lower()

    lung_alfa = len(alfabet)
    sqrt_lung_alfa = int(lung_alfa**(1/2))

    if operatie == 'criptare':

        cod_caracter = {' ':(str(sqrt_lung_alfa + 1), str(sqrt_lung_alfa + 1))}
        for k in range(0, lung_alfa):
            cod_caracter[alfabet[k]] = (str(k // sqrt_lung_alfa), str(k % sqrt_lung_alfa))

        mesaj_criptat = ''
        for caracter in mesaj:
            mesaj_criptat += cod_caracter[caracter][0] + cod_caracter[caracter][1]

        return mesaj_criptat

    else:

        cod_pereche_cifre = np.zeros((sqrt_lung_alfa + 2, sqrt_lung_alfa + 2), dtype = str)
        cod_pereche_cifre[sqrt_lung_alfa + 1][sqrt_lung_alfa + 1] = ' '
        k = 0
        for i in range(0, sqrt_lung_alfa):
            for j in range(0, sqrt_lung_alfa):
                cod_pereche_cifre[i][j] = alfabet[k]
                k += 1

        lungime_mesaj = len(mesaj)

        mesaj_decriptat = ''
        k = 0
        while k < lungime_mesaj:
            mesaj_decriptat += cod_pereche_cifre[int(mesaj[k])][int(mesaj[k + 1])]
            k += 2

        return mesaj_decriptat

def bifid(mesaj, alfabet, operatie):

    mesaj = mesaj.lower()

    lung_alfa = len(alfabet)
    sqrt_lung_alfa = int(lung_alfa ** (1 / 2))

    cod_caracter = {}
    for k in range(0, lung_alfa):
        cod_caracter[alfabet[k]] = (str(k // sqrt_lung_alfa), str(k % sqrt_lung_alfa))

    cod_pereche_cifre = np.zeros((sqrt_lung_alfa + 1, sqrt_lung_alfa + 1), dtype=str)
    k = 0
    for i in range(0, sqrt_lung_alfa):
        for j in range(0, sqrt_lung_alfa):
            cod_pereche_cifre[i][j] = alfabet[k]
            k += 1

    if ' ' not in cod_caracter.keys():
        mesaj = sterge_spatii(mesaj)

    if operatie == 'criptare':

        mesaj_criptat_partial = ''
        for caracter in mesaj:
            mesaj_criptat_partial += cod_caracter[caracter][0]

        for caracter in mesaj:
            mesaj_criptat_partial += cod_caracter[caracter][1]

        mesaj_criptat = ''

        lung_mesaj_criptat_partial = len(mesaj_criptat_partial)
        for k in range(0, lung_mesaj_criptat_partial, 2):
            mesaj_criptat += cod_pereche_cifre[int(mesaj_criptat_partial[k])][int(mesaj_criptat_partial[k + 1])]

        return mesaj_criptat

    else:
        lung_mesaj = len(mesaj)
        mesaj_decriptat_partial = np.zeros(lung_mesaj * 2, dtype = int)
        k = 0
        for litera in mesaj:
            mesaj_decriptat_partial[k] = cod_caracter[litera][0]
            mesaj_decriptat_partial[k + 1] = cod_caracter[litera][1]
            k += 2

        mesaj_decriptat = ''
        for k in range(0, lung_mesaj):
            mesaj_decriptat += cod_pereche_cifre[mesaj_decriptat_partial[k]][mesaj_decriptat_partial[k + lung_mesaj]]

        return mesaj_decriptat

def __compara_coloane(col1, col2): # compara doua coloane, vectori de caractere din numpy
    ord1 = col1[-1]
    ord2 = col2[-1]
    if ord1 < ord2:
        return -1
    elif ord1 == ord2:
        return 0
    else:
        return 1

def __compara_coloane_2(col1, col2):
    ord1 = int(col1[-1])
    ord2 = int(col2[-1])
    if ord1 < ord2:
        return -1
    elif ord1 == ord2:
        return 0
    else:
        return 1

def __compara_litere(lit1, lit2):
    ord1 = ord(lit1[0])
    ord2 = ord(lit2[0])
    if ord1 < ord2:
        return -1
    elif ord1 == ord2:
        return 0
    else:
        return 1

def adfgvx(mesaj, alfabet, cheie, operatie):

    cheie = cheie.lower()
    lung_cheie = len(cheie)

    mesaj = mesaj.lower()
    lung_mesaj = len(mesaj)

    lung_alfa = len(alfabet)
    sqrt_lung_alfa = int(lung_alfa ** (1 / 2))

    if lung_alfa == 25:
        cod = ('a', 'd', 'f', 'g', 'x')
        cod_index = {'a': 0, 'd': 1, 'f': 2, 'g': 3, 'x': 4}
    else:
        cod = ('a', 'd', 'f', 'g', 'v', 'x', 'z')
        cod_index = {'a': 0, 'd': 1, 'f': 2, 'g': 3, 'v' : 4, 'x': 5, 'z': 6}

    cod_caracter = {}
    for k in range(0, lung_alfa):
        cod_caracter[alfabet[k]] = (cod[k // sqrt_lung_alfa], cod[k % sqrt_lung_alfa])

    cod_pereche_cifre = np.zeros((sqrt_lung_alfa + 1, sqrt_lung_alfa + 1), dtype=str)
    k = 0
    for i in range(0, sqrt_lung_alfa):
        for j in range(0, sqrt_lung_alfa):
            cod_pereche_cifre[i][j] = alfabet[k]
            k += 1

    if operatie == 'criptare':

        if ' ' not in alfabet:
            mesaj = sterge_spatii(mesaj)

        mesaj_substituit = ''

        for caracter in mesaj:
            mesaj_substituit += cod_caracter[caracter][0] + cod_caracter[caracter][1]

        matrice_criptare = [] # lista care retine coloanele matricei, pentru facilitarea sortarii
        lung_max_coloana = math.ceil(lung_mesaj*2 / lung_cheie)
        for i in range(0, lung_cheie):
            coloana = np.zeros((lung_max_coloana + 1,), dtype = str)
            matrice_criptare.append(coloana)

        ind_mesaj_substituit = 0
        lung_mesaj_substituit = len(mesaj_substituit)
        for i in range(0, lung_max_coloana): # merge la fiecare element de pe pozitia i...
            for j in range(0, lung_cheie): # ...a fiecarei coloane din lista de coloane (matrice)
                if ind_mesaj_substituit >= lung_mesaj_substituit:
                    break
                matrice_criptare[j][i] = mesaj_substituit[ind_mesaj_substituit]
                ind_mesaj_substituit += 1

        for index, coloana in enumerate(matrice_criptare):
            coloana[-1] = cheie[index]

        matrice_criptare.sort(key = cmp_to_key(__compara_coloane))

        mesaj_criptat = ''
        for j in range(0, lung_cheie):
            for i in range(0, lung_max_coloana):
                if str(matrice_criptare[j][i]).isalpha():
                    mesaj_criptat += matrice_criptare[j][i]
            mesaj_criptat += ' '

        return mesaj_criptat

    else:

        matrice_decriptare = []
        lung_col_max = 0

        for coloana in mesaj.split(' '):
            coloana += ' '
            col = np.array([caracter for caracter in coloana], dtype=object)
            lung_col_max = max(lung_col_max, len(col))
            matrice_decriptare.append(col)

        cheie_cu_indecsi = [(litera, index) for index, litera in enumerate(cheie)]

        print(cheie_cu_indecsi)

        cheie_cu_indecsi.sort(key = cmp_to_key(__compara_litere))

        print(cheie_cu_indecsi)

        for j in range(0, lung_cheie):
            matrice_decriptare[j][-1] = str(cheie_cu_indecsi[j][1])

        matrice_decriptare.sort(key = cmp_to_key(__compara_coloane_2))

        for j in range(0, lung_cheie):
            matrice_decriptare[j][-1] = ''

        mesaj_decriptat_partial = ''
        for i in range(0, lung_col_max):
            for j in range(0, lung_cheie):
                if i < len(matrice_decriptare[j]):
                    mesaj_decriptat_partial += matrice_decriptare[j][i]

        print(mesaj_decriptat_partial)

        mesaj_decriptat = ''
        index = 0
        while index < lung_mesaj - lung_cheie:
            mesaj_decriptat += cod_pereche_cifre[cod_index[mesaj_decriptat_partial[index]]][cod_index[mesaj_decriptat_partial[index + 1]]]
            index += 2

        return mesaj_decriptat




if __name__ == '__main__':
    a = adfgvx("zzgf vgxx azzg vadx dvd adfd adz gfgv vag ada afza adda gxga ddxd afav vfz dgd zafa vgxx", """NA1C3H8TB2OME5WRPD4F6G7I9J0KLQSUVXYZ.,?!         """.lower(),
               'BOMBARDINOCROCODILO', 'decriptare')
    print(a)

"La soare roata se mareste, la umbra numai carnea creste"