from sympy.matrices.exceptions import NonInvertibleMatrixError

from ..Algoritmi import Basic
from ..Algoritmi import Polybius
from ..Algoritmi import Enigma
from ..Algoritmi import DigrafSub
from ..Algoritmi import Rivest
from ..Algoritmi import Hashing
from ..Algoritmi import Block

# fiecare algoritm are o functie specifica de validare (in afara de variantele unui algoritm)
# fiecare functie de validare returneaza un raspuns si un cod
# pentru cod 0, atunci nu a fost gasita nici o eroare si este returnat mesajul criptat/decriptat/spart
# pentru cod 1, returneaza un mesaj de eroare

# subfunctiile de validare (de ex, _verify_duplicate_values) returneaza o valoare diferita de None daca este gasita vreo eroare

# verifica, caractere duplicate in alfabet
def _verify_duplicate_values(entry_vals):

    duplicate_values = set()

    for entry in entry_vals["alfabet"]:

        if entry in duplicate_values:
            return "Matricea conține caractere duplicate!"
        duplicate_values.add(entry)

    return None

# verifica, caractere nedefinite in mesaj
def _undefined_characters(input_text, alfabet):

    input_text = input_text.lower()
    alfabet = alfabet.lower()
    undefined_chars = set()
    special_cases = ["i", "j"]

    for char_text in input_text:
        if char_text in special_cases:
            if "i" not in alfabet and "j" not in alfabet:
                undefined_chars.add("i/j")
        elif char_text != " " and char_text not in alfabet:
                undefined_chars.add(char_text)
    if undefined_chars:
        return f"Mesajul conține caractere nedefinite în alfabet: {', '.join(sorted(undefined_chars))}"
    else:
        return None

# functie de validare pt cifrul lui cezar
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

# functie de validare pt cifrul lui vigenere
def _validate_vigenere(input_text, options):

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie litere ale alfabetului englez si spatii!", 1

    cheie = options['cheie']

    for char in cheie:
        if not char.isalpha():
            return "Cheia trebuie sa fie formata doar din litere ale alfabetului englez!", 1

    return Basic.vignere(input_text, cheie, options['operatie']), 0

# functie de validare pt cifrul lui polybius
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

# functie de validare pt cifrul bifid
def _validate_bifid(input_text, options):

    alfabet = options['alfabet']

    dup_vals = _verify_duplicate_values(options)
    if dup_vals:
        return dup_vals, 1

    undef_chars = _undefined_characters(input_text, alfabet)
    if undef_chars:
       return undef_chars, 1

    return Polybius.bifid(input_text, alfabet, options['operatie']), 0

# functie de validare pt cifrul adfgvx
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

        rez = _undefined_characters(input_text, alfabet)
        if rez:
            return rez, 1
    else:

        adfgvx_decrypt_list = ["a", "d", "f", "g", "v", "x", "z", " "]
        for char in input_text:
            if char not in adfgvx_decrypt_list:
                return "Mesajul criptat poate fi format doar din {'A', 'D', 'F', 'G', 'V', 'X', 'Z'} și spații!", 1

        input_text_words = input_text.split()
        if len(input_text_words) != len(key):
            return "Numărul de cuvinte din mesajul criptat trebuie să fie egal cu lungimea cheii!", 1

    return Polybius.adfgvx(input_text, alfabet, key, options['operatie']), 0

# validarea cheii
def _key_validation_playfair(key):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    invalid_chars = []
    for letter in key:
        if letter not in valid_chars:
            valid_chars.append(letter)
    if invalid_chars:
        return f"Mesajul conține caractere invalide: {', '.join(sorted(invalid_chars))}"

    return None

# functie de validare pt cifrul playfair
def _validate_playfair(input_text, options):

    operation = options['operatie']
    cheie = options['cheie']

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    invalid_chars = []
    for letter in input_text:
        if letter not in valid_chars:
            valid_chars.append(letter)
    if invalid_chars:
        return f"Mesajul conține caractere invalide: {', '.join(sorted(invalid_chars))}", 1

    rez = _key_validation_playfair(cheie)
    if rez:
        return rez, 1

    return DigrafSub.playfair(input_text, cheie, operation), 0

# validarea cheii
def _hill_validation_key(key):

    key_len = len(key)

    if key_len != 4 and key_len != 9:
        return f"Cheia {key} nu are strict 4 sau 9 caractere."

    try:
        import numpy, sympy
        sqrt_len_key = 2 if key_len == 4 else 3
        key_matrix = numpy.zeros((sqrt_len_key, sqrt_len_key), dtype = int)
        key_index = 0

        for i in range(0, sqrt_len_key):
            for j in range(0, sqrt_len_key):
                key_matrix[i][j] = ord(key[key_index]) - 97
                key_index += 1

        sympy.Matrix(key_matrix).inv_mod(26)

    except NonInvertibleMatrixError:
        return f"Matricea formată din caracterele cheii nu este inversabilă. Schimbarea unui caracter poate rezolva eroarea."

    return None

# functie de validare pt cifrul hill
def _validate_hill(input_text, options):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    invalid_chars = []
    for letter in input_text:
        if letter not in valid_chars:
            valid_chars.append(letter)
    if invalid_chars:
        return f"Mesajul conține caractere invalide: {', '.join(sorted(invalid_chars))}", 1

    cheie = options['cheie']
    operation = options['operatie']

    rez = _hill_validation_key(cheie)
    if rez:
        return rez, 1

    return DigrafSub.hill(input_text, cheie, operation), 0

# folosita la decriptare
def rc4_validation_cypher(message):

    valid_chars = []

    for LOWER_letter in range(97, 103):
        valid_chars.append(chr(LOWER_letter))

    for digit in range(48, 58):
        valid_chars.append(chr(digit))

    for i in range(0, len(message)):
        if message[i] not in valid_chars:
            return f"Mesajul tău conține caractere invalide: {message[i]}"

    return None

# functie de validare pt cifrul rivest
def _validate_rc4(input_text, options):

    key = options['cheie']
    operation = options['operatie']

    if operation == "decriptare":
        rez = rc4_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Rivest.rc4(input_text, key, operation), 0

# folosita la decriptare
def _aes128_validation_cypher(message):

    if len(message.replace(" ", "")) % 2 != 0:
        return f"Mesajul este de lungime invalidă."

    valid_chars = [' ']

    for LOWER_letter in range(97, 103):
        valid_chars.append(chr(LOWER_letter))

    for digit in range(48, 58):
        valid_chars.append(chr(digit))

    for i in range(0, len(message)):
        if message[i] not in valid_chars:
            return f"Mesajul tău conține caractere invalide: {message[i]}."
        else:
            pass

    return None

# validarea cheii
def _key_validation_aes(key, expected_length, format):

    valid_chars = []

    if format == 'hexazecimal':
        for LOWER_letter in range(97, 103):
            valid_chars.append(chr(LOWER_letter))

        for digit in range(48, 58):
            valid_chars.append(chr(digit))

        for i in range(0, len(key)):
            if key[i] not in valid_chars:
                return f"Mesajul tău conține caractere invalide: {key[i]}"

    if format == 'hexazecimal':
        expected_length *= 2

    key_len = len(key)
    if int(key_len) != expected_length:
        return f"Cheia {key} nu are strict {expected_length} caractere"
    return None

# functie de validare pt standardul avansat de criptare
def _validate_aes(input_text, options):

    operation = options['operatie']
    key = options['cheie']
    type = options['tip']
    format_key = options['format_cheie'].lower()

    expected_length = 16 if type == 'AES-128' else 32

    rez = _key_validation_aes(key, expected_length, format_key)
    if rez:
        return rez, 1

    if operation == "decriptare":
        rez = _aes128_validation_cypher(input_text)
        if rez:
            return rez, 1

    return Block.aes(input_text, key, format_key, operation), 0

# validarea nu are sens pt hashing
def _hashing(input_text, options):

    varianta = options['varianta']
    if varianta == 'SHA-1':
        return Hashing.sha_1(input_text)
    elif varianta == 'SHA-256':
        return Hashing.sha_256(input_text)

    return None

# folosita atat la criptare cat si decriptare (deoarece operatiile sunt confundate)
def _enigma_validation_cypher_plain(message):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    invalid_chars = []
    for letter in message:
        if letter not in valid_chars:
            valid_chars.append(letter)
    if invalid_chars:
        return f"Mesajul conține caractere invalide: {', '.join(sorted(invalid_chars))}", 1

    return None

# verifica tabloul de comutare (?)
def _plugboard_validation(key):

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    invalid_chars = []
    for letter in key:
        if letter not in valid_chars:
            valid_chars.append(letter)
    if invalid_chars:
        return f"Tabloul conține caractere invalide: {', '.join(sorted(invalid_chars))}"

    counter = 0
    used_chars = []
    white_space_count = 0

    for i in range(len(key)):
        if key[i] in used_chars:
            return f"Caracterul: \"{key[i]}\" nu are voie să se repete."

        if key[i] != " ":
            counter += 1
            used_chars.append(key[i])
            white_space_count = 0
        else:
            if counter == 1:
                return f"Caracterul \"{key[i - 1]}\" nu are pereche."

            counter = 0
            white_space_count += 1

        if white_space_count == 2 or counter == 3:
            return f"Tabloul comutator nu respecta cerintele de formatare"

    if counter == 1:
        return f"\'{key[-1]}\' nu are pereche"

    return None

# transforma lista de perechi de litere intr-un dictionar
def _from_array2dict(arr):

    enigma_dict = {}

    groups = [group for group in arr.split(" ")]

    for i in range(len(groups)):
        enigma_dict.update({groups[i][0]: groups[i][1]})

    return enigma_dict

# functie de validare pt enigma
def _validate_enigma(input_text, options):

    reflector = options['reflector']
    rotor1 = options['rotor1']
    rotor2 = options['rotor2']
    rotor3 = options['rotor3']
    plugboard = options['tablou']

    if 'spec_rotor' in options:
        spec_rotor = options['spec_rotor']
    else: spec_rotor = None

    model = options['model'] # 1, 3 sau 4

    if model not in ('1', '3', '4'):
        raise ValueError('model poate fii 1, (m)3 sau (m)4 (shark)')

    rez = _plugboard_validation(plugboard)
    if rez:
        return rez, 1

    tablou = _from_array2dict(plugboard)  # tablou devine dictionar,
        # fiecare pereche de litere devine o pereche cheie:valoare,
        # unde cheia e prima litera, iar valoarea e a doua litera

    rez = _enigma_validation_cypher_plain(input_text)
    if rez:
        return rez, 1

    if model == '1' or model == '3':
        return Enigma.enigma1(input_text, reflector, rotor1, rotor2, rotor3, tablou)
    else:
        return Enigma.enigma4(input_text, reflector, spec_rotor, rotor1, rotor2, rotor3, tablou)

# functia apelata de frontend pentru accesarea backend-ului
def main_validator(algorithm_name, input_text, options):

    validator_dict = {'cezar':_validate_cezar, 'vigenere':_validate_vigenere, 'polybius':_validate_polybius,
                            'adfgvx':_validate_adfgvx, 'bifid':_validate_bifid, 'playfair':_validate_playfair,
                            'hill':_validate_hill, 'rc4':_validate_rc4,'aes':_validate_aes, 'enigma':_validate_enigma,
                      'hashing':_hashing}

    # verificari preliminatorii

    if algorithm_name not in validator_dict.keys():
        raise ValueError("Numele algoritmului nu este definit.")

    if type(options) != dict:
        raise ValueError("Argumentul 'options' trebuie sa fie de tip dict!")

    if options['operatie'] not in ('criptare', 'decriptare', 'spargere'):
        raise ValueError("Operatia trebuie sa fie 'criptare', 'decriptare' sau 'spargere'.")

    # returneaza valiarea fiecarui algoritm in parte, dupa nume si mesaj input
    return validator_dict[algorithm_name](input_text, options)

if __name__ == '__main__':

    options = {
               'tip':'AES-128',
               'format_cheie':'hexazecimal',
               'cheie':'12345678123456781234567812345678',
               'operatie': 'criptare'
               }

    a = main_validator('aes', 'salut', options)
    print(a)



