import numpy as np

def sha_1(mesaj):

    mesaj_binar = ''

    for caracter in mesaj:
        caracter_binar = bin(ord(caracter))[2::]

        while len(caracter_binar) < 8:
            caracter_binar = '0' + caracter_binar

        mesaj_binar += caracter_binar

    lung_mesaj_binar = len(mesaj_binar)

    i = 0
    lista_blocuri = []
    while i <= lung_mesaj_binar:
        lista_blocuri.append(mesaj_binar[i:min(i + 512, lung_mesaj_binar)])

    for bloc in lista_blocuri:
        ...

    return mesaj_binar

if __name__ == '__main__':
    print(sha_1('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))