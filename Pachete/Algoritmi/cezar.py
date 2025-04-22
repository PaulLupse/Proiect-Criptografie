import numpy as np

litere_mici = np.array((chr(litera) for litera in range(97, 123)))
litere_mari = np.array((chr(litera) for litera in range(65, 91)))

# functie de criptare ce foloseste cifrul lui Caesar
# primeste mesajul (string), numărul de poziții (după care sunt schimbate literele) și acțiunea (criptare sau decriptare)
def cezar(mesaj, nr_pozitii, actiune):

    nr_pozitii %= 26

    if actiune == 'criptare':
        mesaj_criptat = np.array([litera for litera in mesaj])

        l = mesaj_criptat.size

        for i in range(0,l):
            if mesaj_criptat[i].islower():
                litera = chr((ord(str(mesaj_criptat[i])) - 97 + nr_pozitii) % 26 + 97)
            else:
                litera = chr((ord(str(mesaj_criptat[i])) - 65 + nr_pozitii) % 26 + 65)
            mesaj_criptat[i] = litera

        return ''.join(mesaj_criptat)
    else:
        mesaj_decriptat = np.array([litera for litera in mesaj])

        l = mesaj_decriptat.size

        for i in range(0, l):
            if mesaj_decriptat[i].islower():
                litera = chr((ord(str(mesaj_decriptat[i])) - 97 - nr_pozitii) % 26 + 97)
            else:
                litera = chr((ord(str(mesaj_decriptat[i])) - 65 - nr_pozitii) % 26 + 65)
            mesaj_decriptat[i] = litera

        return ''.join(mesaj_decriptat)


def main():
    print(cezar('abcd', 29, 'decriptare'))

if __name__ == '__main__':
    main()
