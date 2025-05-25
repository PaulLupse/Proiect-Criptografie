from ..Algoritmi import Basic
from ..Algoritmi import Polybius
from ..Algoritmi import Enigma
from ..Algoritmi import DigrafSub
from ..Algoritmi import Rivest
from ..Algoritmi import Hashing
from ..Algoritmi import Block
from ..Utilități import Utilities

# functiile de validare returneaza o valoare diferita de 0 daca este gasita vreo eroare
# astfel, la validare, verificam daca functia returneaza ceva
# daca da, atunci avem o Eroare: deci o returnam, impreuna cu codul 1
# daca nu este gasita nicio Eroare: este returnat mesajul criptat/decriptat/spart impreuna cu codul 0

def _verify_duplicate_values(entry_vals):

    duplicate_values = set()

    for entry in entry_vals["matrix_entry"]:
        value = entry.get()
        if value in duplicate_values:
            return "Matricea conține caractere duplicate!", 1
        duplicate_values.add(value)

    return None

def _undefined_characters(input_text, alphabet):

    input_text = input_text.lower()
    alphabet = alphabet.lower()
    undefined_chars = set()
    special_cases = ["i", "j"]

    for char_text in input_text:
        if char_text in special_cases:
            if "i" not in alphabet and "j" not in alphabet:
                undefined_chars.add("i/j")
        elif char_text != " "and char_text not in alphabet:
                undefined_chars.add(char_text)
    if undefined_chars:
        return f"Mesajul conține caractere nedefinite în alfabet: {', '.join(sorted(undefined_chars))}"
    else:
        return None

def _valideaza_cezar(input_text, optiuni):

    cheie = None
    try:
        cheie = int(optiuni['cheie'])
    except ValueError:
        return "Cheia trebuie sa fie un număr!", 1

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie format din litere ale alfabetului englez si spatii!", 1

    if optiuni['operatie'] != 'spargere':
        if cheie < -100 or cheie > 100:
            return "Cheia trebuie sa fie in intervalul [-100, 100]!", 1

    return Basic.cezar(input_text, cheie, optiuni['operatie']), 0

def _valideaza_vigenere(input_text, optiuni):

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie litere ale alfabetului englez si spatii!", 1

    cheie = optiuni['cheie']

    for char in cheie:
        if not char.isalpha():
            return "Cheia trebuie sa fie formata doar din litere ale alfabetului englez!", 1

    return Basic.vignere(input_text, cheie, optiuni['operatie']), 0

def _valideaza_polybius(input_text, optiuni):

    alphabet = optiuni['alphabet']

    dup_vals = _verify_duplicate_values(optiuni)
    if dup_vals:
        return dup_vals, 1

    if optiuni['operatie'] == 'criptare':
        undef_chars = _undefined_characters(input_text, alphabet)
        if undef_chars:
            return undef_chars, 1

    else:
        size_combobox = optiuni["size_combobox"].get()
        digits_text = input_text.replace(" ", "")

        for char in input_text:
            if not (char.isdigit() or char.isspace()):
                return "Mesajul trebuie să conțină doar cifre și spații!", 1

        if len(digits_text) % 2 != 0:
            return "Mesajul trebuie să conțină un număr par de cifre!", 1

        if size_combobox == "5x5":
            for digit in digits_text:
                if int(digit) < 0 or int(digit) > 4:
                    return "Cifrele trebuie să fie cuprinse între 0 și 4!", 1

        if size_combobox == "6x6":
            for digit in digits_text:
                if int(digit) < 0 or int(digit) > 5:
                    return "Cifrele trebuie să fie cuprinse între 0 și 5!", 1

        if size_combobox == "7x7":
            for digit in digits_text:
                if int(digit) < 0 or int(digit) > 6:
                    return "Cifrele trebuie să fie cuprinse între 0 și 6!", 1

    return Polybius.polybius(input_text, alphabet, optiuni['operatie']), 0

def _valideaza_bifid(input_text, optiuni):

    alphabet = optiuni['alphabet']

    dup_vals = _verify_duplicate_values(optiuni)
    if dup_vals:
        return dup_vals, 1

    undef_chars = _undefined_characters(input_text, alphabet)
    if undef_chars:
       return undef_chars, 1

    return Polybius.bifid(input_text, alphabet, optiuni['operatie']), 0

def _valideaza_adfgvx(input_text, optiuni):

    alphabet = optiuni['alphabet']
    key = optiuni['cheie']

    if optiuni['operatie'] == 'criptare':
        ok = False
        for char in alphabet:
            if char == " ":
                ok = True

        if ok:
            if len(input_text) < len(key) // 2:
                return "Lungimea mesajului (cu spații) trebuie să fie cel puțin jumătate din lungimea cheii!", 1
        else:
            input_text = input_text.replace(" ", "")
            if len(input_text) < len(key) // 2:
                return "Lungimea mesajului (fără spații) trebuie să fie cel puțin jumătate din lungimea cheii!", 1
    else:

        adfgvx_decrypt_list = ["a", "d", "f", "g", "v", "x", "z", " "]
        for char in input_text:
            if char not in adfgvx_decrypt_list:
                return "Mesajul poate fi format doar din {'A', 'D', 'F', 'G', 'V', 'X', 'Z'} și spații!", 1

        input_text_words = input_text.split()
        if len(input_text_words) != len(key):
            return "Numărul de cuvinte din mesaj trebuie să fie egal cu lungimea cheii!", 1

    return Polybius.adfgvx(input_text, alphabet, key, optiuni['operatie']), 0

def _playfair_validation_plain(message):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in message:
        if letter not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide: {letter}."

    return message

def _playfair_validation_cypher(message):

    valid_chars = []

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for letter in message:
        if letter not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide:{letter}."

    return message

def _key_validation_playfair(key):

    valid_chars = []

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for letter in key:
        if letter not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide: {letter}."

    return None

def _valideaza_playfair(input_text, optiuni):

    mod = optiuni['operatie']
    cheie = optiuni['cheie']

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in input_text:
        if letter not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide:{letter}.", 1

    rez = _key_validation_playfair(cheie)
    if rez:
        return rez, 1

    return DigrafSub.playfair(input_text, cheie, mod), 0

def _hill_validation_key(key):
    key_len = len(key)

    if key_len != 4 and key_len != 9:
        return f"Cheia {key} nu are strict 4 sau 9 caractere."
    elif key_len == 4:
        square_matrix2 = []
        k = 0

        for i in range(2):
            row = []
            for j in range(2):
                row.append(ord(key[k]))
                k += 1
            square_matrix2.append(row)


        delta = Utilities.second_order_det(square_matrix2)

        if delta == 0:
            return f"Matricea {square_matrix2} nu este inversabilă, determinantul este egal cu {delta}. Schimbarea unui caracter poate rezolva eroarea."

    else:
        square_matrix3 = []
        k = 0

        for i in range(3):
            row = []
            for j in range(3):
                row.append(ord(key[k]))
                k += 1
            square_matrix3.append(row)

        delta = Utilities.third_order_det(square_matrix3)

        if delta == 0:
            return f"Matricea {square_matrix3} nu este inversabilă, pentru că determinantul este egal cu: {delta}. Schimbarea unui caracter poate rezolva eroarea."

    return None

def _valideaza_hill(input_text, optiuni):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in input_text:
        if letter not in valid_chars:
            return f"Mesajul tău conține caractere invalide: {letter}", 1

    cheie = optiuni['cheie']
    mod = optiuni['operatie']

    rez = _hill_validation_key(cheie)
    if rez:
        return rez, 1

    return DigrafSub.hill(input_text, cheie, mod), 0

def rc4_validation_plain(message):
    return None

def rc4_validation_cypher(message):

    valid_chars = []

    for LOWER_letter in range(97, 103):
        valid_chars.append(chr(LOWER_letter))

    for digit in range(48, 58):
        valid_chars.append(chr(digit))

    for i in range(0, len(message)):
        if message[i] not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide:{message[i]}"

    return None

def key_validation(key):
    return None

def _valideaza_rc4(input_text, optiuni):

    cheie = optiuni['cheie']
    mod = optiuni['operatie']

    if mod == "decriptare":
        rez = rc4_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Rivest.rc4(input_text, cheie, mod), 0

def _aes128_validation_cypher(message):

    if len(message.replace(" ", "")) % 2 != 0:
        return f"Eroare: mesajul este de lungime invalidă."

    valid_chars = [' ']

    for LOWER_letter in range(97, 103):
        valid_chars.append(chr(LOWER_letter))

    for digit in range(48, 58):
        valid_chars.append(chr(digit))

    for i in range(0, len(message)):
        if message[i] not in valid_chars:
            return f"Eroare: mesajul tău conține caractere invalide:{message[i]}."
        else:
            pass

    return None

def _key_validation_aes(key, expected_length, format):

    valid_chars = []

    if format == 'hex':
        for LOWER_letter in range(97, 103):
            valid_chars.append(chr(LOWER_letter))

        for digit in range(48, 58):
            valid_chars.append(chr(digit))

        for i in range(0, len(key)):
            if key[i] not in valid_chars:
                return f"Eroare: mesajul tău conține caractere invalide:{key[i]}"

    if format == 'hex':
        expected_length *= 2

    key_len = len(key)
    if int(key_len) != expected_length:
        return f"Cheia {key} nu are strict {expected_length} caractere"
    return None

def _valideaza_aes(input_text, optiuni):

    mod = optiuni['operatie']
    cheie = optiuni['cheie']
    tip = optiuni['tip']
    format_cheie = optiuni['format_cheie']

    expected_length = 16 if tip == '128' else 32

    rez = _key_validation_aes(cheie, expected_length, format_cheie)
    if rez:
        return rez, 1

    if mod == "decriptare":
        rez = _aes128_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Block.aes(input_text, cheie, format_cheie, mod), 0

def _hashing(input_text, optiuni):

    varianta = optiuni['varianta']
    if varianta == 'SHA-1':
        return Hashing.sha_1(input_text)
    elif varianta == 'SHA-256':
        return Hashing.sha_256(input_text)

    return None

def _enigma_validation_cypher_plain(message):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in message:
        if letter not in valid_chars:
            return f"Eroare, mesajul tău conține caractere invalide: {letter}"

    return None

def _check_whitespaces(space):

    counter = 0
    used_chars = []
    white_space_count = 0

    for i in range(len(space)):
        if space[i] in used_chars:
            return f"Eroare, \"{space[i]}\" nu are voie să se repete."

        if space[i] != " ":
            counter += 1
            used_chars.append(space[i])
            white_space_count = 0
        else:
            if counter == 1:
                return f"Eroare, caracterul \"{space[i - 1]}\" nu are pereche."

            counter = 0
            white_space_count += 1

        if white_space_count == 2 or counter == 3:
            return f"Eroare, \"{space[i]}\" nu respecta cerintele de formatare"

    if counter == 1:
        return f"Eroare, \'{space[-1]}\' nu are pereche"

    return None

def _plugboard_validation(key):

    rez = _check_whitespaces(key)
    if rez:
        return rez, 1

    return None

def _from_array2dict(arr):

    enigma_dict = {}

    groups = [group for group in arr.split(" ")]

    for i in range(len(groups)):
        enigma_dict.update({groups[i][0]: groups[i][1]})

    return enigma_dict

def _valideaza_enigma(input_text, optiuni):

    operatie = optiuni['operatie']
    reflector = optiuni['reflector']
    rotor1 = optiuni['rotor1']
    rotor2 = optiuni['rotor2']
    rotor3 = optiuni['rotor3']
    tablou = optiuni['tablou']

    if 'spec_rotor' in optiuni:
        spec_rotor = optiuni['spec_rotor']
    else: spec_rotor = None

    model = optiuni['model'] # 1, 3 sau 4

    if model not in ('1', '3', '4'):
        raise ValueError('Modelul poate fii 1, (m)3 sau (m)4 (shark)')

    rez = _plugboard_validation(tablou)
    if rez:
        return rez, 1

    tablou = _from_array2dict(tablou)  # tablou devine dictionar,
        # fiecare pereche de litere devine o pereche cheie:valoare,
        # unde cheia e prima litera, iar valoarea e a doua litera

    rez = _enigma_validation_cypher_plain(input_text)
    if rez:
        return rez, 1

    if model == '1' or model == '3':
        return Enigma.enigma1(input_text, reflector, rotor1, rotor2, rotor3, tablou)
    else:
        return Enigma.enigma4(input_text, reflector, spec_rotor, rotor1, rotor2, rotor3, tablou)

def main_validator(nume_algoritm, text_intrare, optiuni):

    dictionar_validatori = {'cezar':_valideaza_cezar, 'vigenere':_valideaza_vigenere, 'polybius':_valideaza_polybius,
                            'adfgvx':_valideaza_adfgvx, 'bifid':_valideaza_bifid, 'playfair':_valideaza_playfair,
                            'hill':_valideaza_hill, 'rc4':_valideaza_rc4,'aes':_valideaza_aes, 'enigma':_valideaza_enigma}

    # verificari preliminatorii

    if nume_algoritm not in dictionar_validatori.keys():
        raise ValueError("Numele algoritmului nu este definit.")

    if type(optiuni) != dict:
        raise ValueError("Argumentul 'optiuni' trebuie sa fie de tip dict!")

    if optiuni['operatie'] not in ('criptare', 'decriptare', 'spargere'):
        raise ValueError("Operatia trebuie sa fie 'criptare', 'decriptare' sau 'spargere'.")

    return dictionar_validatori[nume_algoritm](text_intrare, optiuni)

if __name__ == '__main__':

    # exemplu de optiune pt enigma
    optiuni = {'mesaj': 'aaaaa',
               'reflector': 'b',
               'spec_rotor': {'rotor': 'beta', 'offset': 1, 'inel': 1},
               'rotor1': {'rotor': 6, 'offset': 10, 'inel': 21},
               'rotor2': {'rotor': 7, 'offset': 15, 'inel': 11},
               'rotor3': {'rotor': 8, 'offset': 20, 'inel': 6},
               'tablou': 'bq cr di ej kw mt os px uz gh',
               'model': '4',
               'operatie': 'criptare'
               }

    a = main_validator('enigma', 'wfypm', optiuni)
    print(a)



