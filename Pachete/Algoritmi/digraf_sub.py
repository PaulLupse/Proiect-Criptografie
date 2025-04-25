import numpy as np

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



def hill():
    ...

if __name__ == '__main__':
    a = playfair('smparmkmnrsrliormktllumxacmrmworebrmmgmbmktlgl', 'monarchy', 'decriptare')
    print(a)