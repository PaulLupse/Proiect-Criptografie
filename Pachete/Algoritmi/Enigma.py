import numpy as np

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

class _Rotor:

    def __init__(self, config, offset, inel, creste):

        if type(config) is not type('a'):
            raise ValueError('Configuratia rotorului trebuie sa fie string!')
        if type(offset) is not type(1):
            raise ValueError('Offset-ul rotorului trebuie sa fie valoare intreaga!')
        if type(inel) is not type(1):
            raise ValueError('Inelul rotorului trebuie sa fie valoare intreaga!')

        offset -= 1
        inel -= 1

        self._pozitii_schimbare = [(ord(poz) - 97 - 8) % 26 for poz in creste]

        self._config = {}
        self._inv_config = {}
        for index, litera in enumerate('abcdefghijklmnopqrstuvwxyz'):
            index_shiftat = (index - inel) % 26
            self._config[litera] = chr((ord(config[index_shiftat]) - 97 + inel) % 26 + 97)
            self._inv_config[chr((ord(config[index_shiftat]) - 97 + inel) % 26 + 97)] = litera

        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def pozitii_schimbare(self):
        return self._pozitii_schimbare

    def schimb(self, litera):
        litera_shiftata = chr((ord(litera) - 97 + self._offset) % 26 + 97)
        return chr((ord(self._config[litera_shiftata]) - 97 - self._offset) % 26 + 97)

    def inv_schimb(self, litera):
        litera_shiftata = chr((ord(litera) - 97 + self._offset) % 26 + 97)
        return chr((ord(self._inv_config[litera_shiftata]) - 97 - self._offset) % 26 + 97)

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

_reflector_config = {'a': 'EJMZALYXVBWFCRQUONTSPIKHGD'.lower(),
                        'b':'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(),
                        'c':'FVPJIAOYEDRZXWGCTKUQSBNMHL'.lower()}

# tablou: dictionar simetric (daca a : b atunci b : a)
def enigma1(mesaj, reflector, rotor1, rotor2, rotor3, tablou):

    mesaj = mesaj.lower()

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
        litera = reflector.schimb(litera)
        litera = rot1.inv_schimb(litera)
        litera = rot2.inv_schimb(litera)
        litera = rot3.inv_schimb(litera)

        litera = interschimbare[litera]

        mesaj_substituit += litera

    return mesaj_substituit

def enigma3(mesaj, reflector, rotor1, rotor2, rotor3, tablou):

    mesaj = mesaj.lower()

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
        litera = reflector.schimb(litera)
        litera = rot1.inv_schimb(litera)
        litera = rot2.inv_schimb(litera)
        litera = rot3.inv_schimb(litera)

        litera = interschimbare[litera]

        mesaj_substituit += litera

    return mesaj_substituit

def enigma4(mesaj, reflector, spec_rotor, rotor1, rotor2, rotor3, tablou):

    mesaj = mesaj.lower()

    spec_rotor_config = {'beta':'LEYJVCNIXWPBQMDRTAKZGFUHOS'.lower(),
                        'gamma':'FSOKANUERHMBTIYCWLQPZXVGJD'.lower()}

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
        litera = spec_rotor.schimb(litera)
        litera = reflector.schimb(litera)
        litera = spec_rotor.inv_schimb(litera)
        litera = rot1.inv_schimb(litera)
        litera = rot2.inv_schimb(litera)
        litera = rot3.inv_schimb(litera)

        litera = interschimbare[litera]

        mesaj_substituit += litera

    return mesaj_substituit

if __name__ == '__main__':

    a = enigma4('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'b',
                {'rotor':'beta', 'offset':1, 'inel':1},
                {'rotor':6, 'offset':10, 'inel':21},
                {'rotor':7, 'offset':15, 'inel':11},
                {'rotor':8, 'offset':20, 'inel':6},
                {'b':'q', 'c':'r', 'd':'i', 'e':'j', 'k':'w', 'm':'t', 'o':'s', 'p':'x', 'u':'z', 'g':'h'})

    # {'b':'q', 'c':'r', 'd':'i', 'e':'j', 'k':'w', 'm':'t', 'o':'s', 'p':'x', 'u':'z', 'g':'h'}

    print(a)

#woksr ghsir bpfwu tuyyu bbvns jyulp ntopz uapfx tduxn
#wo ksrgh sirbp fw utqyyub bv nsjyu lpnto pzuapf xtdexn