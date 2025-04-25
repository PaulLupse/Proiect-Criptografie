import numpy as np
import math
from functools import cmp_to_key

def __sterge_spatii(mesaj):
    i = 0
    while i < len(mesaj):
        if mesaj[i] == ' ':
            mesaj = mesaj[0:i:] + mesaj[i + 1::]
        else:
            i += 1
    return mesaj

# mesajul este format strict din caracterele ce apar in alfabet
# alfabet-ul poate contine litere (a-z), cifre (0-9) si/sau caractere speciale (alese de utilizator)
def polybius(mesaj, alfabet, operatie):

    mesaj = mesaj.lower()
    # in cazul in care 'j' nu este inclus in alfabet, acesta va fii considerat egal cu 'i'
    if 'j' not in alfabet and 'i' in alfabet:
        for i in range(0, len(mesaj)):
            if mesaj[i] == 'j':
                mesaj = mesaj[0:i:] + 'i' + mesaj[i + 1::]

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

# mesajul este format strict din caracterele ce apar in alfabet
# alfabet-ul poate contine litere (a-z), cifre (0-9) si/sau caractere speciale (alese de utilizator)
def bifid(mesaj, alfabet, operatie):

    mesaj = mesaj.lower()

    # in cazul in care 'j' nu este inclus in alfabet, acesta va fii considerat egal cu 'i'
    if 'j' not in alfabet and 'i' in alfabet:
        for i in range(0, len(mesaj)):
            if mesaj[i] == 'j':
                mesaj = mesaj[0:i:] + 'i' + mesaj[i + 1::]


    lung_alfa = len(alfabet)
    sqrt_lung_alfa = int(lung_alfa ** (1 / 2))

    # fiecarui caracter din alfabet ii atribuim un 'cod' (format din cate doua litere din tuplul cod),
    # dupa linia si coloana pe care se afla in matricea alfabetului
    cod_caracter = {}
    for k in range(0, lung_alfa):
        cod_caracter[alfabet[k]] = (str(k // sqrt_lung_alfa), str(k % sqrt_lung_alfa))

    # inversa operatiei anterioare, atribuim fiecarei pereche de indecsi caracterul corespunzator
    # din matricea alfabetului
    cod_pereche_cifre = np.zeros((sqrt_lung_alfa + 1, sqrt_lung_alfa + 1), dtype=str)
    k = 0
    for i in range(0, sqrt_lung_alfa):
        for j in range(0, sqrt_lung_alfa):
            cod_pereche_cifre[i][j] = alfabet[k]
            k += 1

    if ' ' not in cod_caracter.keys():
        mesaj = __sterge_spatii(mesaj)

    if operatie == 'criptare':

        # inlocuim fiecare caracter cu codul corespunzator,
        # dar intai transcriem prima cifra din cod, apoi a doua

        mesaj_criptat_partial = ''
        for caracter in mesaj:
            mesaj_criptat_partial += cod_caracter[caracter][0]

        for caracter in mesaj:
            mesaj_criptat_partial += cod_caracter[caracter][1]

        mesaj_criptat = ''

        # mesajul criptat constituie substituirea fiecarei pereche de cifre consecutive (care actioneaza ca indecsi),
        # cu caracterul corespunzator din matricea alfabetului
        lung_mesaj_criptat_partial = len(mesaj_criptat_partial)
        for k in range(0, lung_mesaj_criptat_partial, 2):
            mesaj_criptat += cod_pereche_cifre[int(mesaj_criptat_partial[k])][int(mesaj_criptat_partial[k + 1])]

        return mesaj_criptat

    else:
        lung_mesaj = len(mesaj)


        # substiutim fiecare caracter din mesajul criptat cu codul acestuia
        mesaj_decriptat_partial = np.zeros(lung_mesaj * 2, dtype = int)
        k = 0
        for litera in mesaj:
            mesaj_decriptat_partial[k] = cod_caracter[litera][0]
            mesaj_decriptat_partial[k + 1] = cod_caracter[litera][1]
            k += 2

        # parcurgem mesajul criptat substituit pana la jumatate, folosindeu-ne practic de doi indecsi
        # astfel, cand primul index este i, celalalt este i + jumatate din lungimea mesajului criptat substituit
        # in acest fel accesam adevaratul cod al fiecarui caracter criptat
        # si transcriem caracterul decriptat, prin accesarea caracterului atribuit perechii de cifre din cod
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

# mesajul este format strict din caracterele ce apar in alfabet
# alfabet-ul poate contine litere (a-z), cifre (0-9) si/sau caractere speciale (alese de utilizator)
def adfgvx(mesaj, alfabet, cheie, operatie):

    cheie = cheie.lower()
    lung_cheie = len(cheie)

    mesaj = mesaj.lower()
    lung_mesaj = len(mesaj)

    # in cazul in care 'j' nu este inclus in alfabet, acesta va fii considerat egal cu 'i'
    if 'j' not in alfabet and 'i' in alfabet:
        for i in range(0, lung_mesaj):
            if mesaj[i] == 'j':
                mesaj = mesaj[0:i:] + 'i' + mesaj[i + 1::]

    lung_alfa = len(alfabet)
    sqrt_lung_alfa = int(lung_alfa ** (1 / 2))

    if lung_alfa == 25: # pentru ADFGX
        cod = ('a', 'd', 'f', 'g', 'x')
        cod_index = {'a': 0, 'd': 1, 'f': 2, 'g': 3, 'x': 4}

    # / A D F G X
    # A . . . . .
    # D . . . . .
    # F . . . . .
    # G . . . . .
    # X . . . . .

    else: # pentru ADFGVXZ
        cod = ('a', 'd', 'f', 'g', 'v', 'x', 'z')
        cod_index = {'a': 0, 'd': 1, 'f': 2, 'g': 3, 'v' : 4, 'x': 5, 'z': 6}

    # / A D F G V X Z
    # A . . . . . . .
    # D . . . . . . .
    # F . . . . . . .
    # G . . . . . . .
    # V . . . . . . .
    # X . . . . . . .
    # Z . . . . . . .


    # fiecarui caracter din alfabet ii atribuim un 'cod' (format din cate doua litere din tuplul cod),
    # dupa linia si coloana pe care se afla in matricea alfabetului
    cod_caracter = {}
    for k in range(0, lung_alfa):
        cod_caracter[alfabet[k]] = (cod[k // sqrt_lung_alfa], cod[k % sqrt_lung_alfa])

    # inversa operatiei anterioare, atribuim fiecarei pereche de indecsi caracterul corespunzator
    # din matricea alfabetului
    cod_pereche_cifre = np.zeros((sqrt_lung_alfa + 1, sqrt_lung_alfa + 1), dtype=str)
    k = 0
    for i in range(0, sqrt_lung_alfa):
        for j in range(0, sqrt_lung_alfa):
            cod_pereche_cifre[i][j] = alfabet[k]
            k += 1

    if operatie == 'criptare':

        # daca spatiul nu este definit in alfabet, il eliminam din mesaj
        if ' ' not in alfabet:
            mesaj = __sterge_spatii(mesaj)

        mesaj_substituit = ''

        # substituim fiecare caracter cu codul sau (determinat de pozitia caracterului in alfabet)
        for caracter in mesaj:
            mesaj_substituit += cod_caracter[caracter][0] + cod_caracter[caracter][1]

        matrice_criptare = [] # lista care retine coloanele matricei, pentru facilitarea sortarii
        lung_max_coloana = math.ceil(lung_mesaj*2 / lung_cheie)
        for i in range(0, lung_cheie):
            coloana = np.zeros((lung_max_coloana + 1,), dtype = str)
            matrice_criptare.append(coloana)

        # trascriem mesajul substituit in matricea de criptare, pe fiecare linie, de la stanga la dreapta
        index_mesaj_substituit = 0
        lung_mesaj_substituit = len(mesaj_substituit)
        for i in range(0, lung_max_coloana): # merge la fiecare element de pe pozitia i...
            for j in range(0, lung_cheie): # ...a fiecarei coloane din lista de coloane (matrice)
                if index_mesaj_substituit >= lung_mesaj_substituit:
                    break
                matrice_criptare[j][i] = mesaj_substituit[index_mesaj_substituit]
                index_mesaj_substituit += 1

        # atribuim fiecarei coloane j caracterul de pe pozitia j din cheie
        for index, coloana in enumerate(matrice_criptare):
            coloana[-1] = cheie[index]

        # sortam coloanele matricei de criptare dupa caracterul atribuit
        matrice_criptare.sort(key = cmp_to_key(__compara_coloane))

        # mesajul criptat constituie fiecare coloana a matricei de criptare, insiruite in urma sortarii
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

        # luam fiecare 'cuvant' din mesajul criptat si il asezam in matricea de criptare
        # astfel incat sa constituie o coloana a matricei
        for coloana in mesaj.split(' '):
            coloana += ' '
            col = np.array([caracter for caracter in coloana], dtype=object)
            lung_col_max = max(lung_col_max, len(col))
            matrice_decriptare.append(col)

        # atribuim fiecarui caracter din cheie un index
        cheie_cu_indecsi = [(litera, index) for index, litera in enumerate(cheie)]

        # pentru a putea aduce matricea la forma 'nesortata', trebuie sa sortam cheia (lexicografic)...
        cheie_cu_indecsi.sort(key = cmp_to_key(__compara_litere))

        # ...atribuim fiecarei coloane j indexul caracterului de pe pozitia j a cheii sortate (lexicografic)...
        for j in range(0, lung_cheie):
            matrice_decriptare[j][-1] = str(cheie_cu_indecsi[j][1]) # pe ultima pozitie din coloana

        # ...apoi rearanjam coloanele matricei, dupa indexul fiecarui caracter,
        # rearanjare realizata prin sortarea coloanelor dupa indexul atribuit
        matrice_decriptare.sort(key = cmp_to_key(__compara_coloane_2))

        # stergem indexul atribuit
        for j in range(0, lung_cheie):
            matrice_decriptare[j][-1] = ''

        # reconstruim mesajul substituit
        mesaj_decriptat_partial = ''
        for i in range(0, lung_col_max):
            for j in range(0, lung_cheie):
                if i < len(matrice_decriptare[j]):
                    mesaj_decriptat_partial += matrice_decriptare[j][i]

        # construim mesajul decriptat
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