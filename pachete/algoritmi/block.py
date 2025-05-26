import numpy as np
from BitVector import BitVector as Bv
import warnings
warnings.filterwarnings('ignore')

# functie ce efectueaza o rotatie circulara spre stanga
# a bitilor unui numar intreg, pe 32 de biti
def __st_rot(numar, nr_pos):

    bin_numar = bin(numar)[2::]
    bin_numar = ('0' * (32 - len(bin_numar))) + bin_numar
    bin_numar = bin_numar[nr_pos::] + bin_numar[:nr_pos:]
    return int(bin_numar, 2)

s_box = (
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
            )
s_box_inv = (
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
            0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
            0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
            0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
            0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
            0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
            0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
            0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
            0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
            0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
            0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
            0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
            0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
            0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
            0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
            )

# functie ce returneaza valoarea din s_box
# in functie de scrierea octetului in hexa
def get_s_box_value(octet):

    linie = octet // 16
    coloana = octet % 16
    rez = int(s_box[linie * 16 + coloana])
    return rez

# functie ce returneaza valoarea din inv_s_box
# in functie de scrierea octetului in hexa
def get_inv_s_box_value(octet):
    linie = octet // 16
    coloana = octet % 16
    rez = int(s_box_inv[linie * 16 + coloana])
    return rez

constanta_runda = (0x00000000, 0x01000000, 0x02000000, 0x04000000,
                   0x08000000,	0x10000000,	0x20000000,	0x40000000,
                   0x80000000,	0x1B000000,	0x36000000)

# substituieste octetii dintr-un (dublu)cuvant cu valorile din s_box
def __substituire_cuvant(cuvant):

    octet1 = get_s_box_value(cuvant % 16 ** 2)
    octet2 = get_s_box_value((cuvant % 16 ** 4) // (16 ** 2))
    octet3 = get_s_box_value((cuvant % 16 ** 6) // (16 ** 4))
    octet4 = get_s_box_value(cuvant // (16 ** 6))

    return octet4 * (16 ** 6) + octet3 * (16 ** 4) + octet2 * (16 ** 2) + octet1

# functie speciala, folosita la expansiunea cheii de criptare
def g(cuvant, runda):

    cuvant = __substituire_cuvant(cuvant)
    cuvant = __st_rot(cuvant, 8)

    return cuvant ^ constanta_runda[runda]

# functie care returneaza octetii unui (dublu)cuvant
def __get_octeti(cuvant):
    octet1 = cuvant % 16 ** 2
    octet2 = (cuvant % 16 ** 4) // (16 ** 2)
    octet3 = (cuvant % 16 ** 6) // (16 ** 4)
    octet4 = cuvant // (16 ** 6)
    return octet4, octet3, octet2, octet1

# functie care substituieste octetii din stare_mesaj
# cu valorile din s_box
def __substituire(stare_mesaj):
    for j in range(0, 4):
        for i in range(0, 4):
            stare_mesaj[i][j] = get_s_box_value(stare_mesaj[i][j])

# functie care substituieste octetii din stare_mesaj
# cu valorile din inv_s_box
def __inv_substituire(stare_mesaj):
    for j in range(0, 4):
        for i in range(0, 4):
            stare_mesaj[i][j] = get_inv_s_box_value(stare_mesaj[i][j])

# functie ce efectueaza o deplasare criculara spre dreapta a liniilor starii mesajului
def __schimba_linii(stare_mesaj):

    stare_mesaj[1][0], stare_mesaj[1][1], stare_mesaj[1][2], stare_mesaj[1][3] = stare_mesaj[1][1], stare_mesaj[1][2], stare_mesaj[1][3], stare_mesaj[1][0] # prima linie este deplasata circular cu o pozitie
    stare_mesaj[2][0], stare_mesaj[2][1], stare_mesaj[2][2], stare_mesaj[2][3] = stare_mesaj[2][2], stare_mesaj[2][3], stare_mesaj[2][0], stare_mesaj[2][1] # prima linie este deplasata circular cu doua pozitii
    stare_mesaj[3][0], stare_mesaj[3][1], stare_mesaj[3][2], stare_mesaj[3][3] = stare_mesaj[3][3], stare_mesaj[3][0], stare_mesaj[3][1], stare_mesaj[3][2] # prima linie este deplasata circular cu trei pozitii

# functie ce efectueaza o deplasare criculara spre stanga a liniilor starii mesajului
def __inv_schimba_linii(stare_mesaj):

    stare_mesaj[1][0], stare_mesaj[1][1], stare_mesaj[1][2], stare_mesaj[1][3] = stare_mesaj[1][3], stare_mesaj[1][0], stare_mesaj[1][1], stare_mesaj[1][2] # prima linie este deplasata circular cu o pozitie
    stare_mesaj[2][0], stare_mesaj[2][1], stare_mesaj[2][2], stare_mesaj[2][3] = stare_mesaj[2][2], stare_mesaj[2][3], stare_mesaj[2][0], stare_mesaj[2][1] # prima linie este deplasata circular cu doua pozitii
    stare_mesaj[3][0], stare_mesaj[3][1], stare_mesaj[3][2], stare_mesaj[3][3] = stare_mesaj[3][1], stare_mesaj[3][2], stare_mesaj[3][3], stare_mesaj[3][0] # prima linie este deplasata circular cu trei pozitii

# functie care adauga cheia de runda la starea mesajului
def __adauga_cheie(stare_mesaj, cuvinte, runda):

    for j in range(0, 4):
        octeti = __get_octeti(cuvinte[4 * runda + j])
        for i in range(0, 4):
            stare_mesaj[i][j] = stare_mesaj[i][j] ^ octeti[i]

MOD = Bv(bitstring='100011011') # necesar pentru inmultirea in campul Galois
matrice_mixare = np.array([[0x2, 0x3, 0x1, 0x1],[0x1, 0x2, 0x3, 0x1],[0x1, 0x1, 0x2, 0x3],[0x3, 0x1, 0x1, 0x2]], dtype = int)

# functie ce efectueaza mixarea coloanelor
# adica o inmultire a starii mesajului cu matricea de mixare
# inmultire realizata in camp finit
def __mixeaza_coloane(stare_mesaj):

    rezultat = np.zeros((4, 4), dtype = int)
    for i in range(4):
        for j in range(4):
            rez = 0
            for k in range(4):
                m = Bv(intVal = matrice_mixare[i][k])
                s = Bv(intVal = stare_mesaj[k][j])
                rezultat_produs = int(m.gf_multiply_modular(s, MOD, 8))
                rez ^= rezultat_produs
            rezultat[i][j] = rez

    return rezultat

matrice_mixare_inv = np.array([[0x0E, 0x0B, 0x0D, 0x09],
[0x09, 0x0E, 0x0B, 0x0D],
[0x0D, 0x09, 0x0E, 0x0B],
[0x0B, 0x0D, 0x09, 0x0E]], dtype = int)

# functie ce efectueaza inversa mixarii coloanelor
# adica o inmultire a starii mesajului cu inversa matricei de mixare
# inmultire realizata in camp finit
def __inv_mixeaza_coloane(stare_mesaj):

    rezultat = np.zeros((4, 4), dtype = int)
    for i in range(4):
        for j in range(4):
            rez = 0
            for k in range(4):
                m = Bv(intVal = matrice_mixare_inv[i][k])
                s = Bv(intVal = stare_mesaj[k][j])
                rezultat_produs = int(m.gf_multiply_modular(s, MOD, 8))
                rez ^= rezultat_produs
            rezultat[i][j] = rez

    return rezultat

# 1 cuvant == 4 octeti
# functie ce realizeaza expansiunea cheii
# returneaza o lista de (dublu)cuvinte, reprezentand (dublu)cuvintele cheilor de runda
def __expansioneaza_cheia(cheie):

    cuvinte_cheie = [] # lista ce memoreaza cheia + cheile de runde generate ulterior

    lung_cheie = len(cheie)
    marime_cheie = lung_cheie/8

    # initial, impartim cheia in 4 sau 8 cuvinte, fiecare cuvant avand 32 biti (4 octeti, 8 valori hexa)
    # 4 cuvinte pentru aes-128, 8 cuvinte pt aes-256
    for i in range(0, lung_cheie, 8):
        cuvant = int(cheie[i:i + 8:], 16)
        cuvinte_cheie.append(cuvant)

    if marime_cheie == 4: # aes-128
        for runda in range(1, 11):
            i = runda * 4
            cuvant0 = cuvinte_cheie[i - 4] ^ g(cuvinte_cheie[i - 1], runda)
            cuvant1 = cuvant0 ^ cuvinte_cheie[i - 3]
            cuvant2 = cuvant1 ^ cuvinte_cheie[i - 2]
            cuvant3 = cuvant2 ^ cuvinte_cheie[i - 1]

            cuvinte_cheie.append(cuvant0)
            cuvinte_cheie.append(cuvant1)
            cuvinte_cheie.append(cuvant2)
            cuvinte_cheie.append(cuvant3)

    elif marime_cheie == 8: # aes-256
        for runda in range(1, 9): # sunt necesare mai putine runde deoarece generam cate 8 (dublu)cuvinte per iteratie
            i = runda * 8
            cuvant0 = cuvinte_cheie[i - 8] ^ g(cuvinte_cheie[i - 1], runda)
            cuvant1 = cuvant0 ^ cuvinte_cheie[i - 7]
            cuvant2 = cuvant1 ^ cuvinte_cheie[i - 6]
            cuvant3 = cuvant2 ^ cuvinte_cheie[i - 5]
            cuvant4 = __substituire_cuvant(cuvant3) ^ cuvinte_cheie[i - 4]
            cuvant5 = cuvant4 ^ cuvinte_cheie[i - 3]
            cuvant6 = cuvant5 ^ cuvinte_cheie[i - 2]
            cuvant7 = cuvant6 ^ cuvinte_cheie[i - 1]

            cuvinte_cheie.append(cuvant0)
            cuvinte_cheie.append(cuvant1)
            cuvinte_cheie.append(cuvant2)
            cuvinte_cheie.append(cuvant3)
            cuvinte_cheie.append(cuvant4)
            cuvinte_cheie.append(cuvant5)
            cuvinte_cheie.append(cuvant6)
            cuvinte_cheie.append(cuvant7)

    return cuvinte_cheie

# padding (pkcs#7)
def __adauga_padding(octeti_mesaj):
    if len(octeti_mesaj) % 16 == 0:
        for i in range(0, 16):
            octeti_mesaj.append(16)
    else:
        pad = 16 - len(octeti_mesaj) % 16
        for i in range(0, pad):
            octeti_mesaj.append(pad)

# aes-128 sau aes-256 in functie de marimea cheii
# modul EBC cu padding pkcs#7
def aes(mesaj, cheie, format_cheie, operatie):

    # daca cheia este de format string, este convertita la format hexa
    if format_cheie == 'string':
        hex_cheie = ''
        for litera in cheie:
            hex_cheie += hex(ord(litera))[2::]
        cheie = hex_cheie

    # expansionam cheia pentru a putea cuprinde toate rundele de criptare
    cuvinte_cheie = __expansioneaza_cheia(cheie)

    # criptarea propriu-zisa
    if operatie == 'criptare':

        # consideram octetii mesajului
        octeti_mesaj = [ord(caracter) for caracter in mesaj]
        __adauga_padding(octeti_mesaj) # adaugam padding

        blocuri_mesaj = []
        for i in range(0, len(octeti_mesaj), 16): # impartim mesajul in blocuri de cate 16 octeti (16 caractere)
            blocuri_mesaj.append(octeti_mesaj[i:i+16:])

        mesaj_criptat = ''
        for bloc_mesaj in blocuri_mesaj: # aplicam criptare pt fiecare bloc de 16 octeti
            stare_mesaj = np.zeros((4, 4), dtype=int)  # matrice care memoreaza toti 16 octeti ai mesajului,
                                                            # care isi schimba valorile pe parcurs
            index_octeti = 0
            for j in range(0, 4):
                for i in range(0, 4):
                    stare_mesaj[i][j] = bloc_mesaj[index_octeti]
                    index_octeti += 1

            # adaugam cheia initiala
            __adauga_cheie(stare_mesaj, cuvinte_cheie, 0)

            # pentru cheie de lungime de 32 de valori hexa (16 octeti, 128 biti): 11 runde
            # pentru cheie de lungime de 64 de valori hexa (32 octeti, 256 biti): 15 runde
            runde = 10 if len(cheie) == 32 else 14
            for runda in range(1, runde):

                __substituire(stare_mesaj)
                __schimba_linii(stare_mesaj)
                stare_mesaj = __mixeaza_coloane(stare_mesaj)
                __adauga_cheie(stare_mesaj, cuvinte_cheie, runda)

            # mixarea coloanelor este omisa in ultima runda
            # deoarece a fost dovedit ca nu contribuie la calitatea criptarii
            __substituire(stare_mesaj)
            __schimba_linii(stare_mesaj)
            __adauga_cheie(stare_mesaj, cuvinte_cheie, runde)

            for j in range(0, 4):
                for i in range(0, 4):
                    if stare_mesaj[i][j] < 16: # pading daca octetul de pe aceasta pozitie este mai mic decat 16
                        mesaj_criptat += '0'
                    mesaj_criptat += hex(stare_mesaj[i][j])[2::]
            mesaj_criptat += ' '

        return mesaj_criptat

    else:

        mesaj = mesaj.lower().replace(' ', '')

        octeti_mesaj = []
        for i in range(0, len(mesaj), 2):
            octeti_mesaj.append(int(mesaj[i:i+2:], 16))

        blocuri_mesaj = []
        for i in range(0, len(octeti_mesaj), 16):  # impartim mesajul in blocuri de cate 16 octeti (16 caractere)
            blocuri_mesaj.append(octeti_mesaj[i:i + 16:])

        mesaj_decriptat = ''
        for bloc_mesaj in blocuri_mesaj: # aplicam decriptare pt fiecare bloc de 16 octeti
            stare_mesaj = np.zeros((4, 4), dtype=int)  # matrice care memoreaza toti 16 octeti ai mesajului
                                                              # care isi schimba valorile pe parcurs
            index_octeti = 0
            for j in range(0, 4):
                for i in range(0, 4):
                    stare_mesaj[i][j] = bloc_mesaj[index_octeti]
                    index_octeti += 1

            # pentru cheie de lungime de 32 de valori hexa (16 octeti, 128 biti): 11 runde
            # pentru cheie de lungime de 64 de valori hexa (32 octeti, 256 biti): 15 runde
            runde = 9 if len(cheie) == 32 else 13
            __adauga_cheie(stare_mesaj, cuvinte_cheie, runde + 1)

            for runda in range(runde, 0, -1):

                __inv_schimba_linii(stare_mesaj)
                __inv_substituire(stare_mesaj)
                __adauga_cheie(stare_mesaj, cuvinte_cheie, runda)
                stare_mesaj = __inv_mixeaza_coloane(stare_mesaj)

            # (de)mixarea coloanelor este omisa in ultima runda
            __inv_schimba_linii(stare_mesaj)
            __inv_substituire(stare_mesaj)
            __adauga_cheie(stare_mesaj, cuvinte_cheie, 0)

            for j in range(0, 4):
                for i in range(0, 4):
                    if stare_mesaj[i][j] > 16: # pading daca octetul de pe aceasta pozitie este mai mic decat 16
                        mesaj_decriptat += chr(int(stare_mesaj[i][j]))
            mesaj_decriptat += ''

        return mesaj_decriptat

if __name__ == '__main__':

    a = aes('eca4a74ae9a7ab4b8785ecbfea01e4e2 d7ece1b0f9a13ff6eeb7ffb0866c7919 e93c747ce2c953af60f5d96a085fa6ec 6f9284d31756e8cff45a3f08da8d5db8', '5468617473206D79204B756E672046755468617473206D79204B756E67204675'.lower().replace(' ', ''), 'hex', 'decriptare')
    print(a)
