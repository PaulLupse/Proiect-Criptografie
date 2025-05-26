import numpy as np

# clasa care implementeaza functionalitatea unui reflector
# fie litera1 o litera data pentru schimb
# litera1 este inlocuita cu litera2, in functie de configuratie
# totodata, litera2 este inlocuita cu litera1, daca este data pentru schimb
# astfel, avem in total 13 perechi (litera1, litera2) pentru substitutie
class _Reflector:

    def __init__(self, config):

        if type(config) is not type('a'):
            raise ValueError('Configuratia reflectorului trebuie sa fie string!')

        self._config = {}
        for index, litera in enumerate('abcdefghijklmnopqrstuvwxyz'):
            self._config[litera] = config[index]
            self._config[config[index]] = litera

    def schimb(self, litera):
        return self._config[litera]

# clasa care implementeaza functionalitatea unui rotor
class _Rotor:

    def __init__(self, config, offset, inel, creste):

        if type(config) is not type('a'):
            raise ValueError('Configuratia rotorului trebuie sa fie string!')
        if type(offset) is not type(1):
            raise ValueError('Offset-ul rotorului trebuie sa fie valoare intreaga!')
        if type(inel) is not type(1):
            raise ValueError('Inelul rotorului trebuie sa fie valoare intreaga!')

        # literele sunt indexate de la 0
        offset -= 1
        inel -= 1

        # pozitiile in care crestele sunt in pozitia clichetului
        # cand acestea sunt atinse, are loc o rotatie a urmatorului rotor
        # iar daca rotorul curent nu este primul rotor, atingerea pozitiilor determina miscarea si rotorului anterior
        # de exemplu, daca rotorul 1 atinge pozitia de schimbare (creasta este in pozitia clichetului),
        # atunci, la urmatoarea mischare a clicheților, rotorul 2 este rotit cu o pozitie,
        # iar rotorul 1 iese din pozitia de schimbare
        # daca rotorul 2, la randul lui, a fost rotit in pozitia de schimbare,
        # urmatoarea rotatie a primului rotor va determina rotatia si celui de-al treilea rotor,
        # dar si rotatia celui de-al doilea, deoarece al treilea clichet va actiona atat rotorul 2
        # cat si rotorul 3
        self._pozitii_schimbare = [(ord(poz) - 97 - 8) % 26 for poz in creste]

        self._config = {}
        self._inv_config = {}
        for index, litera in enumerate('abcdefghijklmnopqrstuvwxyz'):

            # schimbarea setarii de inel (ringstellung) are ca efect o substituire asemenea cifrului lui cezar,
            # dar in directia opusa, astfel, daca setarea de inel este 02-B, intrarea 'a' va fii considerata 'z'
            # deoarece cheia 'a' este setata cu o pozite inapoi, desi, din afara, semnalul pare sa intre in cheia 'a',
            # iar operatiile de substitutie ulterioare, in care semnalul intra in pozitia 'a'
            # se vor realiza in functie de litera 'z'
            # totodata, o data cu schimbarea setarii de inel, are loc schimbarea locatiilor crestelor

            index_shiftat = (index - inel) % 26

            # trebuie sa consideram faptul ca schimbarea setarii de inel determina deplasarea si pozitiei de iesire
            # cu atatea pozitii cu cat este schimbata starea de inel
            # de exemplu, daca setarea de inel este 02-B, semnalul intra in cheia 'a' care este considerata 'z'
            # daca 'z' este conectat la iesirea 'j', atunci semnalul de iesire va fii, de fapt, 'k'
            # adica deplasat cu o pozitie (in alfabet)

            self._config[litera] = chr((ord(config[index_shiftat]) - 97 + inel) % 26 + 97)
            self._inv_config[chr((ord(config[index_shiftat]) - 97 + inel) % 26 + 97)] = litera

        self._offset = offset

    # returneaza offset-ul rotorului (pozitia in care se afla, relativ de origine)
    @property
    def offset(self):
        return self._offset

    # returneaza acele pozitii care, daca sunt atinse, vor determina actiunea clicheului asupra urmatorului rotor
    @property
    def pozitii_schimbare(self):
        return self._pozitii_schimbare

    # face schimbul literei cu o alta, in functie de setarile interne si offset-ul rotorului
    def schimb(self, litera):

        # schimbarea setarii de inel (ringstellung) are ca efect o substituire asemenea cifrului lui cezar,
        # daca rotorul este mutat in pozitia 02-B, semnalul intrat prin cheia 'a' va fii considerat 'b'
        # adica deplasat in fata cu o pozitie.

        # pozitia de iesire este si ea schimbata, doar in directia opusa
        # astfel, daca rotorul este in pozitia 02-B, semnalul intra prin cheia 'a', este considerat 'b',
        # si daca litera 'b' este conectata la litera 'k', semanul de iesire va trece prin cheia 'j'
        # adica deplasat in spate cu o pozitia

        litera_shiftata = chr((ord(litera) - 97 + self._offset) % 26 + 97)
        return chr((ord(self._config[litera_shiftata]) - 97 - self._offset) % 26 + 97)

        # pozitia rotorului are, mai mult sau mai putin, un efect invers fata de setarea de inel
        # de exemplu, fie ca rotorul sa aiba setarea de inel 02-B,
        # deci fiecare semnal de intrare este deplasat in spate cu o pozitie,
        # totodata, fie ca rotorul sa fie pe pozitia 02-B,
        # deci fiecare semnal de intrare este deplasat in fata cu o pozite,
        # efectul este o anulare a deplasarii pozitiilor, intrucat semanlul intrand prin cheia 'a' va fii considerat 'a'
        # deplasarea pozitiei de iesire este si ea anulata, din aceleasi motive
        # astfel, daca litera 'a' este conectata la 'e', semnalul de iesire va fii tot 'e'

    # face inversul schimbul literei cu o alta, in functie de setarile interne si offset-ul rotorului
    # utilizata la 'intoarcerea' semnalului prin rotori
    def inv_schimb(self, litera):
        litera_shiftata = chr((ord(litera) - 97 + self._offset) % 26 + 97)
        return chr((ord(self._inv_config[litera_shiftata]) - 97 - self._offset) % 26 + 97)

    # efectueaza deplasarea cu o pozitie a rotorului
    def rotire(self):
        self._offset = (self._offset + 1) % 26

_rotor_config = np.array(['EKMFLGDQVZNTOWYHXUSPAIBRCJ/Y'.lower(),
                    'AJDKSIRUXBLHWTMCQGZNPYFVOE/M'.lower(),
                    'BDFHJLCPRTXVZNYEIWGAKMUSQO/D'.lower(),
                    'ESOVPZJAYQUIRHXLNFTGKDCMWB/R'.lower(),
                    'VZBRGITYUPSDNHLXAWMJQOFECK/H'.lower(),
                    'JPGVOUMFYQBENHZRDKASXLICTW/HU'.lower(),
                    'NZJHGRCXMYSWBOUFAIVLPEKQDT/HU'.lower(),
                    'FKQHTLXOCBJSPDZRAMEWNIUYGV/HU'.lower()], dtype = object)

_reflector_config = {'UKW A': 'EJMZALYXVBWFCRQUONTSPIKHGD'.lower(),
                        'UKW B':'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(),
                        'UKW C':'FVPJIAOYEDRZXWGCTKUQSBNMHL'.lower()}

# tablou: dictionar
def enigma1(mesaj, reflector, rotor1, rotor2, rotor3, tablou):

    mesaj = mesaj.lower()

    interschimbare = {} # dictionar simetric, daca a:b atunci b:a
    for key, value in tablou.items():
        interschimbare[key] = value
        interschimbare[value] = key

    for litera in 'abcdefghijklmnopqrstuvwxyz':
        try:
            interschimbare[litera]
        except: # daca litera nu a fost 'conectata' in tablou la o alta litera,
            interschimbare[litera] = litera # aceasta va fii schimbata cu ea insasi

    # rotoarele sunt notate de la stanga la dreapta
    # desi operatiunea acestora este, practic, configurata de la dreapta la stanga
    reflector = _Reflector(_reflector_config[reflector])
    rot1 = _Rotor(_rotor_config[rotor1['rotor'] - 1], rotor1['offset'], rotor1['inel'],
                  _rotor_config[rotor1['rotor'] - 1][27:])
    rot2 = _Rotor(_rotor_config[rotor2['rotor'] - 1], rotor2['offset'], rotor2['inel'],
                  _rotor_config[rotor2['rotor'] - 1][27:])
    rot3 = _Rotor(_rotor_config[rotor3['rotor'] - 1], rotor3['offset'], rotor3['inel'],
                  _rotor_config[rotor3['rotor'] - 1][27:])

    mesaj_substituit = ''
    for litera in mesaj:

        if litera == ' ':
            mesaj_substituit += ' '
            continue

        # dupa ce este apasata o tasta, semnalul intai trece prin tabloul de comutare
        litera = interschimbare[litera]

        rotire_2 = False
        rotire_1 = False

        if rot3.offset in rot3.pozitii_schimbare: # daca primul rotor (din dreapta) este in pozitia de rotire
            rotire_2 = True # rotorul 2 se va rotii

        if rot2.offset in rot2.pozitii_schimbare: # daca al doilea rotor (din dreapta) este in pozitia de rotire
            rotire_1 = True # al treilea rotor (din dreapta) se va rotii

        rot3.rotire()

        if rotire_2:
            rot2.rotire()
        if rotire_1: # daca rotorul 3 se va rotii, va determina rotirea atat a rotorului 3,
                     # cat si a rotorului 2
            rot2.rotire()
            rot1.rotire()

        # semnalul trece prin cele 3 rotoare
        litera = rot3.schimb(litera)
        litera = rot2.schimb(litera)
        litera = rot1.schimb(litera)
        # este schimbat cu un alt semnal in reflector
        litera = reflector.schimb(litera)
        # si se intoarce prin cele 3 rotoare
        litera = rot1.inv_schimb(litera)
        litera = rot2.inv_schimb(litera)
        litera = rot3.inv_schimb(litera)

        # la final, trecand dinnou prin tabloul de comutare
        litera = interschimbare[litera]

        mesaj_substituit += litera

    return mesaj_substituit

def enigma4(mesaj, reflector, spec_rotor, rotor1, rotor2, rotor3, tablou):

    mesaj = mesaj.lower()

    # rotoarele speciale sunt statice, nu se misca pe parcursul criptarii
    # desi pot fii miscate, iar setarea de inel de asemenea poate fii schimbata
    spec_rotor_config = {'Beta':'LEYJVCNIXWPBQMDRTAKZGFUHOS'.lower(),
                        'Gamma':'FSOKANUERHMBTIYCWLQPZXVGJD'.lower()}

    # prezenta rotoarelor speciale este singura diferenta de la modelul 1 si 3

    interschimbare = {}
    for key, value in tablou.items():
        interschimbare[key] = value
        interschimbare[value] = key

    for litera in 'abcdefghijklmnopqrstuvwxyz':
        try:
            interschimbare[litera]
        except:
            interschimbare[litera] = litera

    reflector = _Reflector(_reflector_config[reflector])
    spec_rotor = _Rotor(spec_rotor_config[spec_rotor['rotor']], spec_rotor['offset'], spec_rotor['inel'], 'a')
    rot1 = _Rotor(_rotor_config[rotor1['rotor'] - 1], rotor1['offset'], rotor1['inel'], _rotor_config[rotor1['rotor'] - 1][27:])
    rot2 = _Rotor(_rotor_config[rotor2['rotor'] - 1], rotor2['offset'], rotor2['inel'], _rotor_config[rotor2['rotor'] - 1][27:])
    rot3 = _Rotor(_rotor_config[rotor3['rotor'] - 1], rotor3['offset'], rotor3['inel'], _rotor_config[rotor3['rotor'] - 1][27:])

    mesaj_substituit = ''
    for litera in mesaj:

        if litera == ' ':
            mesaj_substituit += ' '
            continue
        litera = interschimbare[litera]

        rotire_2 = False
        rotire_1 = False

        if rot3.offset in rot3.pozitii_schimbare:
            rotire_2 = True

        if rot2.offset in rot2.pozitii_schimbare:
            rotire_1 = True

        rot3.rotire()

        if rotire_2:
            rot2.rotire()
        if rotire_1:
            rot2.rotire()
            rot1.rotire()

        litera = rot3.schimb(litera)
        litera = rot2.schimb(litera)
        litera = rot1.schimb(litera)
        # este inclus rotorul speical,
        litera = spec_rotor.schimb(litera)
        litera = reflector.schimb(litera)
        # imclusiv la 'intoarcere'
        litera = spec_rotor.inv_schimb(litera)
        litera = rot1.inv_schimb(litera)
        litera = rot2.inv_schimb(litera)
        litera = rot3.inv_schimb(litera)

        litera = interschimbare[litera]

        mesaj_substituit += litera

    return mesaj_substituit

#woksr ghsir bpfwu tuyyu bbvns jyulp ntopz uapfx tduxn
#wo ksrgh sirbp fw utqyyub bv nsjyu lpnto pzuapf xtdexn