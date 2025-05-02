import numpy as np

def rc4(mesaj, cheie, operatie):

    lung_cheie = len(cheie)
    lung_mesaj = len(mesaj)

    permutare = np.array([i for i in range(0, 256)], dtype = int)
    cheie_extinsa = np.zeros((256,), dtype = int)
    index_cheie = 0
    for i in range(0, 256):
        cheie_extinsa[i] = ord(cheie[index_cheie])
        index_cheie = (index_cheie + 1) % lung_cheie

    j = 0
    for i in range (0, 256):
        j = (j + permutare[i] + cheie_extinsa[i % lung_cheie]) % 256
        permutare[i], permutare[j] = permutare[j], permutare[i]

    cheie_curenta = np.zeros((lung_mesaj,), dtype = int)
    i = 0; j = 0
    while i < lung_mesaj:
        i = (i + 1) % 256
        j = (j + permutare[i]) % 256
        permutare[i], permutare[j] = permutare[j], permutare[i]
        k = (permutare[i] + permutare[j]) % 256
        cheie_curenta[i - 1] = permutare[k]

    for element in cheie_curenta:
        print(hex(element)[2::], end = '')
    print()

    if operatie == 'criptare':
        mesaj_criptat = ''
        for index, litera in enumerate(mesaj):
            valoare = hex(int(cheie_curenta[index]) ^ ord(litera))[2::]
            valoare = '0' * (2 - len(valoare)) + valoare
            mesaj_criptat += valoare
        return mesaj_criptat
    else:
        mesaj_decriptat = ''
        index_mesaj = 0
        index_cheie_curenta = 0
        while index_mesaj < lung_mesaj:
            octet = int(mesaj[index_mesaj:index_mesaj + 2:], 16)
            mesaj_decriptat += chr(int(cheie_curenta[index_cheie_curenta]) ^ octet)
            index_mesaj += 2
            index_cheie_curenta += 1
        return mesaj_decriptat

if __name__ == '__main__':
    print(rc4('0ffee550fb405c8cd7f3cfb45d9846ec806e34d07e0490c255de4995299c06b8136be21d2deea95871951a9b81ffbd7204faf88219119b51766c6573c7efa386adc8c3611381bf30e88d5d15d057d4236ae2f452beb4e588ca4a22f6804255f700cadc47488e8c53f45bf036b54f68d5f067437b94d092', 'Riga', 'decriptare'))

'La soare roata se mareste, la umbra numai carnea creste. Si somn e carnea, se dezumfla, dar fring si umbra iar o umfla.'