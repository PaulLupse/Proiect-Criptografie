from ..Algoritmi import Basic
from ..Algoritmi import Polybius
from ..Algoritmi import Enigma
from ..Algoritmi import DigrafSub
from ..Algoritmi import Rivest
from ..Algoritmi import Hashing
from ..Algoritmi import Block
from ..Utilități import Utilities

# subfunctiile de validare returneaza o valoare diferita de 0 daca este gasita vreo eroare
# astfel, la validare, verificam daca functia returneaza ceva
# daca da, atunci avem o Eroare: deci o returnam, impreuna cu codul 1
# daca nu este gasita nicio Eroare: este returnat mesajul criptat/decriptat/spart impreuna cu codul 0

def _verify_duplicate_values(entry_vals):

    duplicate_values = set()

    for entry in entry_vals["alfabet"]:

        if entry in duplicate_values:
            return "Matricea conține caractere duplicate!", 1
        duplicate_values.add(entry)

    return None

def _undefined_characters(input_text, alfabet):

    input_text = input_text.lower()
    alfabet = alfabet.lower()
    undefined_chars = set()
    special_cases = ["i", "j"]

    for char_text in input_text:
        if char_text in special_cases:
            if "i" not in alfabet and "j" not in alfabet:
                undefined_chars.add("i/j")
        elif char_text != " "and char_text not in alfabet:
                undefined_chars.add(char_text)
    if undefined_chars:
        return f"Mesajul conține caractere nedefinite în alfabet: {', '.join(sorted(undefined_chars))}"
    else:
        return None

def _validate_cezar(input_text, options):

    try:
        cheie = int(options['cheie'])
    except ValueError:
        return "Cheia trebuie sa fie un număr!", 1

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie format din litere ale alfabetului englez si spatii!", 1

    if options['operatie'] != 'spargere':
        if cheie < -100 or cheie > 100:
            return "Cheia trebuie sa fie in intervalul [-100, 100]!", 1

    return Basic.cezar(input_text, cheie, options['operatie']), 0

def _validate_vigenere(input_text, options):

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie litere ale alfabetului englez si spatii!", 1

    cheie = options['cheie']

    for char in cheie:
        if not char.isalpha():
            return "Cheia trebuie sa fie formata doar din litere ale alfabetului englez!", 1

    return Basic.vignere(input_text, cheie, options['operatie']), 0

def _validate_polybius(input_text, options):

    alfabet = options['alfabet']

    dup_vals = _verify_duplicate_values(options)
    if dup_vals:
        return dup_vals, 1

    if options['operatie'] == 'criptare':
        undef_chars = _undefined_characters(input_text, alfabet)
        if undef_chars:
            return undef_chars, 1

    else:
        size_combobox = options["marime_matrice"]
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

    return Polybius.polybius(input_text, alfabet, options['operatie']), 0

def _validate_bifid(input_text, options):

    alfabet = options['alfabet']

    dup_vals = _verify_duplicate_values(options)
    if dup_vals:
        return dup_vals, 1

    undef_chars = _undefined_characters(input_text, alfabet)
    if undef_chars:
       return undef_chars, 1

    return Polybius.bifid(input_text, alfabet, options['operatie']), 0

def _validate_adfgvx(input_text, options):

    alfabet = options['alfabet']
    key = options['cheie']

    dup_vals = _verify_duplicate_values(options)
    if dup_vals:
        return dup_vals, 1

    if options['operatie'] == 'criptare':
        ok = False
        for char in alfabet:
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

    return Polybius.adfgvx(input_text, alfabet, key, options['operatie']), 0

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

def _validate_playfair(input_text, options):

    operation = options['operatie']
    cheie = options['cheie']

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

    return DigrafSub.playfair(input_text, cheie, operation), 0

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

def _validate_hill(input_text, options):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in input_text:
        if letter not in valid_chars:
            return f"Mesajul tău conține caractere invalide: {letter}", 1

    cheie = options['cheie']
    operation = options['operatie']

    rez = _hill_validation_key(cheie)
    if rez:
        return rez, 1

    return DigrafSub.hill(input_text, cheie, operation), 0

def rc4_validation_plain():
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

def _validate_rc4(input_text, options):

    key = options['cheie']
    operation = options['operatie']

    if operation == "decriptare":
        rez = rc4_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Rivest.rc4(input_text, key, operation), 0

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

def _validate_aes(input_text, options):

    operation = options['operatie']
    key = options['cheie']
    type = options['tip']
    format_key = options['format_cheie']

    expected_length = 16 if type == '128' else 32

    rez = _key_validation_aes(key, expected_length, format_key)
    if rez:
        return rez, 1

    if operation == "decriptare":
        rez = _aes128_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Block.aes(input_text, key, format_key, operation), 0

def _hashing(input_text, options):

    varianta = options['varianta']
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

def _validate_enigma(input_text, options):

    reflector = options['reflector']
    rotor1 = options['rotor1']
    rotor2 = options['rotor2']
    rotor3 = options['rotor3']
    plugboard = options['tablou']

    if 'spec_rotor' in options:
        spec_rotor = options['spec_rotor']
    else: spec_rotor = None

    operationel = options['operationel'] # 1, 3 sau 4

    if operationel not in ('1', '3', '4'):
        raise ValueError('operationelul poate fii 1, (m)3 sau (m)4 (shark)')

    rez = _plugboard_validation(plugboard)
    if rez:
        return rez, 1

    tablou = _from_array2dict(plugboard)  # tablou devine dictionar,
        # fiecare pereche de litere devine o pereche cheie:valoare,
        # unde cheia e prima litera, iar valoarea e a doua litera

    rez = _enigma_validation_cypher_plain(input_text)
    if rez:
        return rez, 1

    if operationel == '1' or operationel == '3':
        return Enigma.enigma1(input_text, reflector, rotor1, rotor2, rotor3, tablou)
    else:
        return Enigma.enigma4(input_text, reflector, spec_rotor, rotor1, rotor2, rotor3, tablou)

def main_validator(algorithm_name, input_text, options):

    validator_dict = {'cezar':_validate_cezar, 'vigenere':_validate_vigenere, 'polybius':_validate_polybius,
                            'adfgvx':_validate_adfgvx, 'bifid':_validate_bifid, 'playfair':_validate_playfair,
                            'hill':_validate_hill, 'rc4':_validate_rc4,'aes':_validate_aes, 'enigma':_validate_enigma}

    # verificari preliminatorii

    if algorithm_name not in validator_dict.keys():
        raise ValueError("Numele algoritmului nu este definit.")

    if type(options) != dict:
        raise ValueError("Argumentul 'options' trebuie sa fie de tip dict!")

    if options['operatie'] not in ('criptare', 'decriptare', 'spargere'):
        raise ValueError("Operatia trebuie sa fie 'criptare', 'decriptare' sau 'spargere'.")

    return validator_dict[algorithm_name](input_text, options)

if __name__ == '__main__':

    # exemplu de optiune pt enigma
    options = {'mesaj': 'aaaaa',
               'reflector': 'b',
               'spec_rotor': {'rotor': 'beta', 'offset': 1, 'inel': 1},
               'rotor1': {'rotor': 6, 'offset': 10, 'inel': 21},
               'rotor2': {'rotor': 7, 'offset': 15, 'inel': 11},
               'rotor3': {'rotor': 8, 'offset': 20, 'inel': 6},
               'tablou': 'bq cr di ej kw mt os px uz gh',
               'operationel': '4',
               'operatie': 'criptare'
               }

    a = main_validator('enigma', 'wfypm', options)
    print(a)



