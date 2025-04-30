import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter.constants import DISABLED, NORMAL
import string
try:
    import CustomWidgets as Cw
except:
    from . import CustomWidgets as Cw
try:
    from ..Algoritmi import basic
    from ..Algoritmi import polybius
except:
    print("IMPORTURILE RELATIVE FUNCTIONEAZA NUMA CAND RULEZI CODUL DIN main.py")

def right_click_menu(widget):
    menu = tk.Menu(widget, tearoff = 0)
    menu.add_command(label = "Copy", command = lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label = "Paste", command = lambda: widget.event_generate("<<Paste>>"))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)

def limit_one_char(event):
    widget = event.widget
    val = widget.get()
    if len(val) > 1:
        widget.delete(1, tk.END)

def generate_polybius_matrix(settings_frame, size_combobox, entry_vals):

    size = 5
    combobox_value = size_combobox.get()
    if combobox_value == "5x5":
        size = 5
    if combobox_value == "6x6":
        size = 6
    if combobox_value == "7x7":
        size = 7

    for widget in settings_frame.winfo_children():
        if not isinstance(widget, tk.Frame):
            widget.destroy()

    for row in range(size):
        if row == size - 1:
            padding_value = (0, 20)
        else:
            padding_value = 0
        row_labels = tk.Label(settings_frame, text=str(row))
        row_labels.grid(row=row + 2, column=0, pady=padding_value)
    for col in range(size):
        col_labels = tk.Label(settings_frame, text=str(col))
        col_labels.grid(row=1, column=col + 2, padx=5)

    polybius_entry = []
    for row in range(size):
        if row == size - 1:
            padding_value = (0, 20)
        else:
            padding_value = 0
        for col in range(size):
            entry = tk.Entry(settings_frame, width=2, justify="center")
            entry.grid(row=row + 2, column=col + 2, pady=padding_value)
            entry.bind("<KeyRelease>", limit_one_char)
            entry.bind("<FocusOut>", limit_one_char)
            polybius_entry.append(entry)
    entry_vals["polybius_entry"] = polybius_entry
    reset_polybius_entry(entry_vals, size_combobox)

def reset_polybius_entry(entry_vals, size_combobox):

    alphabet = []
    combobox_value = size_combobox.get()
    for c in range(ord('a'), ord('z') + 1):
        if chr(c) != 'j':
            alphabet.append(chr(c))

    if combobox_value == "5x5":
        for i, entry in enumerate(entry_vals["polybius_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

    alphabet = alphabet + [char for char in string.digits] + [char for char in string.punctuation]
    if combobox_value == "6x6":
        for i, entry in enumerate(entry_vals["polybius_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

    if combobox_value == "7x7":
        for i, entry in enumerate(entry_vals["polybius_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

def update_settings(combobox, settings_frame, entry_vals):

    for widget in settings_frame.winfo_children():
        widget.destroy()

    entry_vals["textbox2"].config(state = NORMAL)
    entry_vals["textbox1"].delete("1.0", "end-1c")
    entry_vals["textbox2"].delete("1.0", "end-1c")

    selected_algorithm = combobox.get()

    if selected_algorithm == "Caesar Cipher":
        caesar_entry = Cw.LabeledEntry(settings_frame, "Cheie de criptare:", "w", 4,0,0)
        caesar_entry.insert(0,"0")
        brute_force_button = ttk.Button(settings_frame, text = "Spargere parolă", width = 23, command = lambda: brute_force_caesar(entry_vals["textbox1"], entry_vals["textbox2"]))
        brute_force_button.grid(row = 1, column = 0)
        entry_vals["caesar_entry"] = caesar_entry

    elif selected_algorithm == "Vigenère Cipher":
        vigenere_textbox = Cw.LabeledTextbox(settings_frame, "Cheie de criptare:", "n",3,15,0,0,1,1)
        entry_vals["vigenere_textbox"] = vigenere_textbox

    elif selected_algorithm == "Polybius":

        matrix_settings_frame = tk.Frame(settings_frame)
        matrix_settings_frame.grid(row = 0, column = 0, columnspan = 10)

        size_combobox = ttk.Combobox(matrix_settings_frame, values = ["5x5","6x6","7x7"], state = "readonly", width = 3)
        size_combobox.set("5x5")
        size_combobox.grid(row = 0, column = 0, columnspan = 5)
        size_combobox.bind("<<ComboboxSelected>>", lambda event: generate_polybius_matrix(settings_frame, size_combobox, entry_vals))
        reset_button = ttk.Button(matrix_settings_frame, text = "Resetare alfabet", command = lambda: reset_polybius_entry(entry_vals, size_combobox))
        reset_button.grid(row = 0, column = 10, columnspan = 5)
        generate_polybius_matrix(settings_frame, size_combobox, entry_vals)

def verify_text(text):

    for char in text:
        if not (char.isalpha() or char.isspace()):
            return False
    return True

def verify_entry_caesar(val):

    if val < -100 or val > 100:
        return False
    return True

def verify_textbox_vigenere(text):

    for char in text:
        if not char.isalpha():
            return False
    return True

def polybius_alphabet(entry_vals):

    alphabet = ""
    duplicate_values = set()
    for entry in entry_vals["polybius_entry"]:
        value = entry.get()
        if value == "":
            alphabet += "  "
        else:
            if value in duplicate_values:
                return
            duplicate_values.add(value)
            alphabet += value
    return alphabet

def verify_polybius(input_text, alphabet):

    input_text = input_text.lower()
    alphabet = alphabet.lower()
    undefined_chars = set()
    special_cases = ["i", "j"]

    for char_text in input_text:
        if char_text in special_cases:
            if "i" not in alphabet and "j" not in alphabet:
                undefined_chars.add("i/j")
        elif char_text != " " and char_text not in alphabet:
            undefined_chars.add(char_text)
    if undefined_chars:
        return undefined_chars
    else:
        return None

def crypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")
    textbox2.config(state = NORMAL)

    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":
        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return

        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", basic.cezar(input_text, shift_value, 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Vigenère Cipher":
        key_value = entry_vals["vigenere_textbox"].get("1.0", "end-1c")
        if not verify_textbox_vigenere(key_value):
            msgbox.showerror("Eroare", "Cheia trebuie să conțină doar litere mari sau mici! (fără spații)")
            return
        if not verify_text(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", basic.vignere(input_text, key_value, 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Polybius":
        alphabet = polybius_alphabet(entry_vals)
        if alphabet is None:
            msgbox.showerror("Eroare", "Matricea conține caractere duplicate!")
            return
        undefined_chars = verify_polybius(input_text, alphabet)
        if verify_polybius(input_text, alphabet):
            msgbox.showerror("Eroare", f"Mesajul conține caractere nedefinite în alfabet: {', '.join(sorted(undefined_chars))}")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", polybius.polybius(mesaj = input_text, alfabet = alphabet, operatie = 'criptare'))
        textbox2.config(state = DISABLED)

def decrypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")
    textbox2.config(state = NORMAL)

    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":
        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", basic.cezar(input_text, shift_value, 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Vigenère Cipher":
        key_value = entry_vals["vigenere_textbox"].get("1.0", "end-1c")
        if not verify_textbox_vigenere(key_value):
            msgbox.showerror("Eroare", "Cheia trebuie să conțină doar litere mari sau mici! (fără spații)")
            return
        if not verify_text(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", basic.vignere(input_text, key_value, 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Polybius":
        alphabet = polybius_alphabet(entry_vals)
        if alphabet is None:
            msgbox.showerror("Eroare", "Matricea conține caractere duplicate!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", polybius.polybius(mesaj = input_text, alfabet = alphabet, operatie = 'decriptare'))
        textbox2.config(state = DISABLED)

def brute_force_caesar(textbox1, textbox2):

    input_text = textbox1.get("1.0", "end-1c")
    textbox2.config(state = NORMAL)

    if not verify_text(input_text):
        msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
        return
    string_list = basic.cezar(input_text, None, 'spargere')
    textbox2.delete("1.0", "end-1c")
    for i, strings in enumerate(string_list, start=1):
        textbox2.insert("end", f"{i}. {strings}\n")
    textbox2.config(state = DISABLED)


def main():

    root = tk.Tk()
    root.resizable(False,False)
    root.title("Algoritmi de Criptare")
    try:
        root.iconbitmap("imagine-lacat.ico")
    except:
        print("Nush")
    entry_vals = {}
    textbox1 = Cw.LabeledTextbox(root, "Text:", "n", 10, 20,0,0,20,1)
    entry_vals["textbox1"] = textbox1
    right_click_menu(textbox1)
    textbox2 = Cw.LabeledTextbox(root, "Text criptat/decriptat:", "n", 10, 20,0,2,20,1)
    entry_vals["textbox2"] = textbox2
    right_click_menu(textbox2)

    options_frame = tk.Frame(root)
    options_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "n")
    settings_frame = tk.Frame(root)
    settings_frame.grid(row = 1, column = 1, sticky = "n")

    combobox = ttk.Combobox(options_frame, values = ["Caesar Cipher","Vigenère Cipher", "Polybius"], state = "readonly")
    combobox.set("Alege algoritmul")
    combobox.grid(row = 0, column = 0, columnspan = 2)
    combobox.bind("<<ComboboxSelected>>", lambda event: update_settings(combobox, settings_frame, entry_vals))

    crypt_button = ttk.Button(options_frame, text = "Criptare", command = lambda: crypt(textbox1, textbox2, combobox, entry_vals))
    crypt_button.grid(row = 1, column = 0)
    decrypt_button = ttk.Button(options_frame, text = "Decriptare", command = lambda: decrypt(textbox1, textbox2, combobox, entry_vals))
    decrypt_button.grid(row = 1, column = 1)

    root.mainloop()

if __name__ == "__main__":
    main()