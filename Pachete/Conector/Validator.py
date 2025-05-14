from ..Algoritmi import Basic
from ..Algoritmi import Polybius
from ..Algoritmi import Enigma
from ..Algoritmi import DigrafSub
from ..Algoritmi import Rivest
from ..Algoritmi import Hashing
from ..Algoritmi import Block

def _verify_duplicate_values(entry_vals):

    duplicate_values = set()

    for entry in entry_vals["matrix_entry"]:
        value = entry.get()
        if value in duplicate_values:
            return "Matricea conține caractere duplicate!", 1
        duplicate_values.add(value)

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

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie format din litere ale alfabetului englez si spatii!", 1

    cheie = None
    if optiuni['operatie'] != 'spargere':
        cheie = optiuni['cheie']
        if cheie < -100 or cheie > 100:
            return "Cheia trebuie sa fie in intervalul [-100, 100]!", 1

    return Basic.cezar(input_text, cheie, optiuni['operatie']), None

def _valideaza_vigenere(input_text, optiuni):

    for char in input_text:
        if not (char.isalpha() or char.isspace()):
            return "Mesajul de intrare trebuie sa fie litere ale alfabetului englez si spatii!", 1

    cheie = optiuni['cheie']

    for char in cheie:
        if not char.isalpha():
            return "Cheia trebuie sa fie formata doar din litere ale alfabetului englez!", 1

    return Basic.vignere(input_text, cheie, optiuni['operatie'])

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

    return Polybius.polybius(input_text, alphabet, optiuni['operatie'])

def _valideaza_bifid(input_text, optiuni):

    alphabet = optiuni['alphabet']

    dup_vals = _verify_duplicate_values(optiuni)
    if dup_vals:
        return dup_vals, 1

    undef_chars = _undefined_characters(input_text, alphabet)
    if undef_chars:
       return undef_chars, 1

    return Polybius.bifid(input_text, alphabet, optiuni['operatie'])

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

    return Polybius.adfgvx(input_text, alphabet, key, optiuni['operatie'])

def is_string(message):
    if type(message) is not str:
        return False
    else:
        return True

def playfair_validation_plain(message):
    if not is_string(message):
        return f"Eroare, {message} nu este un sir de caractere."

    valid_chars = [" "]

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for UPPER_letter in range(65, 91):
        valid_chars.append(chr(UPPER_letter))

    for letter in message:
        if letter not in valid_chars:
            return "Eroare, mesajul tău conține caractere invalide."

    return message

def playfair_validation_cypher(message):
    if not is_string(message):
        return f"Eroare, {message} nu este un sir de caractere."

    valid_chars = []

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for letter in message:
        if letter not in valid_chars:
            return "Eroare, mesajul tău conține caractere invalide."

    return message

def key_validation_playfair(key):
    if not is_string(key):
        return f"Eroare, {key} nu este un sir de caractere."

    valid_chars = []
    used_chars = []

    for LOWER_letter in range(97, 123):
        valid_chars.append(chr(LOWER_letter))

    for letter in key:
        if letter in used_chars:
            letter_freq = key.count(letter)
            return f"Eroare, cheia nu poate avea caractere care se repetă, caracterul \"{letter}\" a fost găsit de {letter_freq} ori."
        if letter not in valid_chars:
            return "Eroare, mesajul tău conține caractere invalide."
        used_chars.append(letter)

    return key

def _valideaza_playfair(message, optiuni):

    mod = optiuni['operatie']
    key = optiuni['cheie']

    error_statement = "Nu au fost îndeplinite toate condițiile de formatare"
    if key_validation_playfair(key) != key:
        return error_statement

    if mod == "criptare":
        return playfair_validation_plain(message)

    elif mod == "decriptare":
        return playfair_validation_cypher(message)

    else:
        return "Modul ales nu este valid."

def main_validator(nume_algoritm, text_intrare, optiuni):

    dictionar_validatori = {'cezar':_valideaza_cezar, 'vigenere':_valideaza_vigenere, 'polybius':_valideaza_polybius,
                            'adfgvx':_valideaza_adfgvx, 'bifid':_valideaza_bifid, 'playfair':None,
                            'hill':None, 'rc4':None,
                            'aes':None}

    return dictionar_validatori[nume_algoritm](text_intrare, optiuni)


