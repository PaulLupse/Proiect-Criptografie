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
    from ..Algoritmi import Basic
    from ..Algoritmi import Polybius
    from ..Algoritmi import Hashing
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

def generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals):

    size = 5
    combobox_value = size_combobox.get()
    if combobox_value == "2x2":
        size = 2
    if combobox_value == "3x3":
        size = 3
    if combobox_value == "5x5":
        size = 5
    if combobox_value == "6x6":
        size = 6
    if combobox_value == "7x7":
        size = 7

    for widget in settings_frame.winfo_children():
        if not isinstance(widget, tk.Frame):
            widget.destroy()

    if combobox.get() == "Hill Cipher":

        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            row_labels = tk.Label(settings_frame, text = str(row))
            row_labels.grid(row = row + 2, column = 0, pady = padding_value)
        for col in range(size):
            col_labels = tk.Label(settings_frame, text = str(col))
            col_labels.grid(row = 1, column = col + 2, padx = 5)

        playfair_entry = []
        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            for col in range(size):
                entry = tk.Entry(settings_frame, width = 2, justify = "center")
                entry.grid(row = row + 2, column = col + 2, pady = padding_value)
                entry.bind("<KeyRelease>", limit_one_char)
                entry.bind("<FocusOut>", limit_one_char)
                playfair_entry.append(entry)
        entry_vals["matrix_entry"] = playfair_entry

    elif combobox.get() == "ADFGVX":

        index_list = ["A" , "D", "F", "G", "V", "X", "Z"]
        index = 0
        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            row_labels = tk.Label(settings_frame, text = index_list[index])
            index += 1
            row_labels.grid(row = row + 3, column = 0, pady = padding_value)
        index = 0
        for col in range(size):
            col_labels = tk.Label(settings_frame, text = index_list[index])
            index += 1
            col_labels.grid(row = 2, column = col + 3, padx = 5)

        adfgvx_entry = []
        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            for col in range(size):
                entry = tk.Entry(settings_frame, width=2, justify="center")
                entry.grid(row=row + 3, column=col + 3, pady=padding_value)
                entry.bind("<KeyRelease>", limit_one_char)
                entry.bind("<FocusOut>", limit_one_char)
                adfgvx_entry.append(entry)
        entry_vals["matrix_entry"] = adfgvx_entry
        reset_polybius_bifid_entry(entry_vals, size_combobox)

    else:

        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            row_labels = tk.Label(settings_frame, text = str(row))
            row_labels.grid(row = row + 2, column = 0, pady = padding_value)
        for col in range(size):
            col_labels = tk.Label(settings_frame, text = str(col))
            col_labels.grid(row = 1, column = col + 2, padx = 5)

        polybius_entry = []
        for row in range(size):
            if row == size - 1:
                padding_value = (0, 20)
            else:
                padding_value = 0
            for col in range(size):
                entry = tk.Entry(settings_frame, width = 2, justify = "center")
                entry.grid(row = row + 2, column = col + 2, pady = padding_value)
                entry.bind("<KeyRelease>", limit_one_char)
                entry.bind("<FocusOut>", limit_one_char)
                polybius_entry.append(entry)
        entry_vals["matrix_entry"] = polybius_entry
        reset_polybius_bifid_entry(entry_vals, size_combobox)

def reset_polybius_bifid_entry(entry_vals, size_combobox):

    alphabet = []
    combobox_value = size_combobox.get()

    if combobox_value == "5x5":
        for c in range(ord('a'), ord('z') + 1):
            if chr(c) != 'j':
                alphabet.append(chr(c))
    else:
        for c in range(ord('a'), ord('z') + 1):
            alphabet.append(chr(c))

    if combobox_value == "5x5":
        for i, entry in enumerate(entry_vals["matrix_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

    if combobox_value in ["6x6", "7x7"]:
        alphabet = alphabet + [char for char in string.digits] + [char for char in string.punctuation]

    if combobox_value == "6x6":
        for i, entry in enumerate(entry_vals["matrix_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

    if combobox_value == "7x7":
        for i, entry in enumerate(entry_vals["matrix_entry"]):
            entry.delete(0, tk.END)
            if i < len(alphabet):
                entry.insert(0, alphabet[i])

def number_to_letter(number):

    if 1 <= number <= 26:
        return chr(64 + number)
    else:
        return ""

def enigma_entry_set(entry, value):

    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, f"{value} {number_to_letter(value)}")
    entry.config(state="readonly")

def increment(entry):

    entry.config(state="normal")
    value = entry.get().split()
    number = int(value[0])
    if number < 26:
        number += 1
    else:
        number = 1
    enigma_entry_set(entry, number)

def decrement(entry):

    entry.config(state="normal")
    value = entry.get().split()
    number = int(value[0])
    if number > 1:
        number -= 1
    else:
        number = 26
    enigma_entry_set(entry, number)

def generate_enigma_options(settings_frame, enigma_version_combobox, entry_vals):

    selected_version = entry_vals["enigma_version_combobox"].get()

    for widget in settings_frame.winfo_children():
        if widget != enigma_version_combobox.master:
            widget.destroy()

    if selected_version == "Enigma I":

        reflector_label = tk.Label(settings_frame, text="Reflector: ")
        reflector_label.grid(row=1, column=4, pady=5)
        reflector_combobox = ttk.Combobox(settings_frame, values=["UKW A", "UKW B", "UKW C"], width=6, state="readonly")
        reflector_combobox.set("UKW A")
        reflector_combobox.grid(row=1, column=5, pady=5)

        enigma_settings_frame = tk.Frame(settings_frame)
        enigma_settings_frame.grid(row=2, column=0, columnspan=10)

        rotor1_label = tk.Label(enigma_settings_frame, text = "Rotor 1")
        rotor1_label.grid(row = 0, column = 0)
        rotor1_combobox = ttk.Combobox(enigma_settings_frame, values = ["I", "II", "III", "IV", "V"], width = 5, state = "readonly", justify = "center")
        rotor1_combobox.set("I")
        rotor1_combobox.grid(row = 1, column = 0)
        rotor2_label = tk.Label(enigma_settings_frame, text = "Rotor 2")
        rotor2_label.grid(row=2, column=0)
        rotor2_combobox = ttk.Combobox(enigma_settings_frame, values = ["I", "II", "III", "IV", "V"], width = 5, state = "readonly", justify = "center")
        rotor2_combobox.set("I")
        rotor2_combobox.grid(row = 3, column = 0)
        rotor3_label = tk.Label(enigma_settings_frame, text = "Rotor 3")
        rotor3_label.grid(row=4, column=0)
        rotor3_combobox = ttk.Combobox(enigma_settings_frame, values = ["I", "II", "III", "IV", "V"], width = 5, state = "readonly", justify = "center")
        rotor3_combobox.set("I")
        rotor3_combobox.grid(row = 5, column = 0)

        enigma_settings_frame.columnconfigure(1, minsize=30)
        enigma_settings_frame.columnconfigure(5, minsize=30)

        position1_label = tk.Label(enigma_settings_frame, text="Poziție")
        position1_label.grid(row=0, column=3)
        minus_button_position1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position1.grid(row=1, column=2)
        minus_button_position1.config(command=lambda: decrement(position1_entry))
        position1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position1_entry.grid(row=1, column=3)
        plus_button_position1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position1.grid(row=1, column=4)
        plus_button_position1.config(command=lambda: increment(position1_entry))

        ring1_label = tk.Label(enigma_settings_frame, text="Inel")
        ring1_label.grid(row=0, column=7, padx=10)
        minus_button_ring1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring1.grid(row=1, column=6)
        minus_button_ring1.config(command=lambda: decrement(ring1_entry))
        ring1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring1_entry.grid(row=1, column=7)
        plus_button_ring1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring1.grid(row=1, column=8)
        plus_button_ring1.config(command=lambda: increment(ring1_entry))

        enigma_entry_set(position1_entry, 1)
        enigma_entry_set(ring1_entry, 1)

        position2_label = tk.Label(enigma_settings_frame, text="Poziție")
        position2_label.grid(row=2, column=3)
        minus_button_position2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position2.grid(row=3, column=2)
        minus_button_position2.config(command=lambda: decrement(position2_entry))
        position2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position2_entry.grid(row=3, column=3)
        plus_button_position2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position2.grid(row=3, column=4)
        plus_button_position2.config(command=lambda: increment(position2_entry))

        ring2_label = tk.Label(enigma_settings_frame, text="Inel")
        ring2_label.grid(row=2, column=7, padx=10)
        minus_button_ring2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring2.grid(row=3, column=6)
        minus_button_ring2.config(command=lambda: decrement(ring2_entry))
        ring2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring2_entry.grid(row=3, column=7)
        plus_button_ring2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring2.grid(row=3, column=8)
        plus_button_ring2.config(command=lambda: increment(ring2_entry))

        enigma_entry_set(position2_entry, 1)
        enigma_entry_set(ring2_entry, 1)

        position3_label = tk.Label(enigma_settings_frame, text="Poziție")
        position3_label.grid(row=4, column=3)
        minus_button_position3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position3.grid(row=5, column=2)
        minus_button_position3.config(command=lambda: decrement(position3_entry))
        position3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position3_entry.grid(row=5, column=3)
        plus_button_position3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position3.grid(row=5, column=4)
        plus_button_position3.config(command=lambda: increment(position3_entry))

        ring3_label = tk.Label(enigma_settings_frame, text="Inel")
        ring3_label.grid(row=4, column=7, padx=10)
        minus_button_ring3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring3.grid(row=5, column=6)
        minus_button_ring3.config(command=lambda: decrement(ring3_entry))
        ring3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring3_entry.grid(row=5, column=7)
        plus_button_ring3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring3.grid(row=5, column=8)
        plus_button_ring3.config(command=lambda: increment(ring3_entry))

        enigma_entry_set(position3_entry, 1)
        enigma_entry_set(ring3_entry, 1)

        plugboard_label = tk.Label(enigma_settings_frame, text="Tablou comutator")
        plugboard_label.grid(row = 6, column = 0, columnspan = 10)
        plugboard_entry = tk.Entry(enigma_settings_frame, width=30, justify="center")
        plugboard_entry.insert(0, "bq cr di ej kw mt os px uz gh")
        plugboard_entry.grid(row = 7, column = 0, columnspan = 10, pady=(0,10))

    elif selected_version == "Enigma M3":

        reflector_label = tk.Label(settings_frame, text="Reflector: ")
        reflector_label.grid(row=1, column=4, pady=5)
        reflector_combobox = ttk.Combobox(settings_frame, values=["UKW B", "UKW C"], width=6, state="readonly")
        reflector_combobox.set("UKW B")
        reflector_combobox.grid(row=1, column=5, pady=5)

        enigma_settings_frame = tk.Frame(settings_frame)
        enigma_settings_frame.grid(row=2, column=0, columnspan=10)

        rotor1_label = tk.Label(enigma_settings_frame, text="Rotor 1")
        rotor1_label.grid(row=0, column=0)
        rotor1_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor1_combobox.set("I")
        rotor1_combobox.grid(row=1, column=0)
        rotor2_label = tk.Label(enigma_settings_frame, text="Rotor 2")
        rotor2_label.grid(row=2, column=0)
        rotor2_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor2_combobox.set("I")
        rotor2_combobox.grid(row=3, column=0)
        rotor3_label = tk.Label(enigma_settings_frame, text="Rotor 3")
        rotor3_label.grid(row=4, column=0)
        rotor3_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor3_combobox.set("I")
        rotor3_combobox.grid(row=5, column=0)

        enigma_settings_frame.columnconfigure(1, minsize=30)
        enigma_settings_frame.columnconfigure(5, minsize=30)

        position1_label = tk.Label(enigma_settings_frame, text="Poziție")
        position1_label.grid(row=0, column=3)
        minus_button_position1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position1.grid(row=1, column=2)
        minus_button_position1.config(command=lambda: decrement(position1_entry))
        position1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position1_entry.grid(row=1, column=3)
        plus_button_position1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position1.grid(row=1, column=4)
        plus_button_position1.config(command=lambda: increment(position1_entry))

        ring1_label = tk.Label(enigma_settings_frame, text="Inel")
        ring1_label.grid(row=0, column=7, padx=10)
        minus_button_ring1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring1.grid(row=1, column=6)
        minus_button_ring1.config(command=lambda: decrement(ring1_entry))
        ring1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring1_entry.grid(row=1, column=7)
        plus_button_ring1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring1.grid(row=1, column=8)
        plus_button_ring1.config(command=lambda: increment(ring1_entry))

        enigma_entry_set(position1_entry, 1)
        enigma_entry_set(ring1_entry, 1)

        position2_label = tk.Label(enigma_settings_frame, text="Poziție")
        position2_label.grid(row=2, column=3)
        minus_button_position2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position2.grid(row=3, column=2)
        minus_button_position2.config(command=lambda: decrement(position2_entry))
        position2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position2_entry.grid(row=3, column=3)
        plus_button_position2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position2.grid(row=3, column=4)
        plus_button_position2.config(command=lambda: increment(position2_entry))

        ring2_label = tk.Label(enigma_settings_frame, text="Inel")
        ring2_label.grid(row=2, column=7, padx=10)
        minus_button_ring2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring2.grid(row=3, column=6)
        minus_button_ring2.config(command=lambda: decrement(ring2_entry))
        ring2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring2_entry.grid(row=3, column=7)
        plus_button_ring2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring2.grid(row=3, column=8)
        plus_button_ring2.config(command=lambda: increment(ring2_entry))

        enigma_entry_set(position2_entry, 1)
        enigma_entry_set(ring2_entry, 1)

        position3_label = tk.Label(enigma_settings_frame, text="Poziție")
        position3_label.grid(row=4, column=3)
        minus_button_position3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position3.grid(row=5, column=2)
        minus_button_position3.config(command=lambda: decrement(position3_entry))
        position3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position3_entry.grid(row=5, column=3)
        plus_button_position3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position3.grid(row=5, column=4)
        plus_button_position3.config(command=lambda: increment(position3_entry))

        ring3_label = tk.Label(enigma_settings_frame, text="Inel")
        ring3_label.grid(row=4, column=7, padx=10)
        minus_button_ring3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring3.grid(row=5, column=6)
        minus_button_ring3.config(command=lambda: decrement(ring3_entry))
        ring3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring3_entry.grid(row=5, column=7)
        plus_button_ring3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring3.grid(row=5, column=8)
        plus_button_ring3.config(command=lambda: increment(ring3_entry))

        enigma_entry_set(position3_entry, 1)
        enigma_entry_set(ring3_entry, 1)

        plugboard_label = tk.Label(enigma_settings_frame, text="Tablou comutator")
        plugboard_label.grid(row=6, column=0, columnspan=10)
        plugboard_entry = tk.Entry(enigma_settings_frame, width=30, justify="center")
        plugboard_entry.insert(0, "bq cr di ej kw mt os px uz gh")
        plugboard_entry.grid(row=7, column=0, columnspan=10, pady=(0, 10))

    if selected_version == 'Enigma M4 "Shark"':

        reflector_label = tk.Label(settings_frame, text="Reflector: ")
        reflector_label.grid(row=1, column=4, pady=5)
        reflector_combobox = ttk.Combobox(settings_frame, values=["UKW B thin", "UKW C thin"], width=10, state="readonly")
        reflector_combobox.set("UKW B thin")
        reflector_combobox.grid(row=1, column=5, pady=5)

        enigma_settings_frame = tk.Frame(settings_frame)
        enigma_settings_frame.grid(row=2, column=0, columnspan=10)

        rotor1_label = tk.Label(enigma_settings_frame, text="Rotor 1")
        rotor1_label.grid(row=0, column=0)
        rotor1_combobox = ttk.Combobox(enigma_settings_frame, values=["Beta", "Gamma"], width=7, state="readonly", justify="center")
        rotor1_combobox.set("Beta")
        rotor1_combobox.grid(row=1, column=0)
        rotor2_label = tk.Label(enigma_settings_frame, text="Rotor 2")
        rotor2_label.grid(row=2, column=0)
        rotor2_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor2_combobox.set("I")
        rotor2_combobox.grid(row=3, column=0)
        rotor3_label = tk.Label(enigma_settings_frame, text="Rotor 3")
        rotor3_label.grid(row=4, column=0)
        rotor3_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor3_combobox.set("I")
        rotor3_combobox.grid(row=5, column=0)
        rotor4_label = tk.Label(enigma_settings_frame, text="Rotor 4")
        rotor4_label.grid(row=6, column=0)
        rotor4_combobox = ttk.Combobox(enigma_settings_frame, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], width=5, state="readonly", justify="center")
        rotor4_combobox.set("I")
        rotor4_combobox.grid(row=7, column=0)

        enigma_settings_frame.columnconfigure(1, minsize=30)
        enigma_settings_frame.columnconfigure(5, minsize=30)

        position1_label = tk.Label(enigma_settings_frame, text="Poziție")
        position1_label.grid(row=0, column=3)
        minus_button_position1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position1.grid(row=1, column=2)
        minus_button_position1.config(command=lambda: decrement(position1_entry))
        position1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position1_entry.grid(row=1, column=3)
        plus_button_position1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position1.grid(row=1, column=4)
        plus_button_position1.config(command=lambda: increment(position1_entry))

        ring1_label = tk.Label(enigma_settings_frame, text="Inel")
        ring1_label.grid(row=0, column=7, padx=10)
        minus_button_ring1 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring1.grid(row=1, column=6)
        minus_button_ring1.config(command=lambda: decrement(ring1_entry))
        ring1_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring1_entry.grid(row=1, column=7)
        plus_button_ring1 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring1.grid(row=1, column=8)
        plus_button_ring1.config(command=lambda: increment(ring1_entry))

        enigma_entry_set(position1_entry, 1)
        enigma_entry_set(ring1_entry, 1)

        position2_label = tk.Label(enigma_settings_frame, text="Poziție")
        position2_label.grid(row=2, column=3)
        minus_button_position2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position2.grid(row=3, column=2)
        minus_button_position2.config(command=lambda: decrement(position2_entry))
        position2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position2_entry.grid(row=3, column=3)
        plus_button_position2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position2.grid(row=3, column=4)
        plus_button_position2.config(command=lambda: increment(position2_entry))

        ring2_label = tk.Label(enigma_settings_frame, text="Inel")
        ring2_label.grid(row=2, column=7, padx=10)
        minus_button_ring2 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring2.grid(row=3, column=6)
        minus_button_ring2.config(command=lambda: decrement(ring2_entry))
        ring2_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring2_entry.grid(row=3, column=7)
        plus_button_ring2 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring2.grid(row=3, column=8)
        plus_button_ring2.config(command=lambda: increment(ring2_entry))

        enigma_entry_set(position2_entry, 1)
        enigma_entry_set(ring2_entry, 1)

        position3_label = tk.Label(enigma_settings_frame, text="Poziție")
        position3_label.grid(row=4, column=3)
        minus_button_position3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position3.grid(row=5, column=2)
        minus_button_position3.config(command=lambda: decrement(position3_entry))
        position3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position3_entry.grid(row=5, column=3)
        plus_button_position3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position3.grid(row=5, column=4)
        plus_button_position3.config(command=lambda: increment(position3_entry))

        ring3_label = tk.Label(enigma_settings_frame, text="Inel")
        ring3_label.grid(row=4, column=7, padx=10)
        minus_button_ring3 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring3.grid(row=5, column=6)
        minus_button_ring3.config(command=lambda: decrement(ring3_entry))
        ring3_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring3_entry.grid(row=5, column=7)
        plus_button_ring3 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring3.grid(row=5, column=8)
        plus_button_ring3.config(command=lambda: increment(ring3_entry))

        enigma_entry_set(position3_entry, 1)
        enigma_entry_set(ring3_entry, 1)

        position4_label = tk.Label(enigma_settings_frame, text="Poziție")
        position4_label.grid(row=6, column=3)
        minus_button_position4 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_position4.grid(row=7, column=2)
        minus_button_position4.config(command=lambda: decrement(position4_entry))
        position4_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        position4_entry.grid(row=7, column=3)
        plus_button_position4 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_position4.grid(row=7, column=4)
        plus_button_position4.config(command=lambda: increment(position4_entry))

        ring4_label = tk.Label(enigma_settings_frame, text="Inel")
        ring4_label.grid(row=6, column=7, padx=10)
        minus_button_ring4 = ttk.Button(enigma_settings_frame, text="-", width=1)
        minus_button_ring4.grid(row=7, column=6)
        minus_button_ring4.config(command=lambda: decrement(ring4_entry))
        ring4_entry = tk.Entry(enigma_settings_frame, width=5, justify="center", state="readonly")
        ring4_entry.grid(row=7, column=7)
        plus_button_ring4 = ttk.Button(enigma_settings_frame, text="+", width=1)
        plus_button_ring4.grid(row=7, column=8)
        plus_button_ring4.config(command=lambda: increment(ring4_entry))

        enigma_entry_set(position4_entry, 1)
        enigma_entry_set(ring4_entry, 1)

        plugboard_label = tk.Label(enigma_settings_frame, text="Tablou comutator")
        plugboard_label.grid(row=8, column=0, columnspan=10)
        plugboard_entry = tk.Entry(enigma_settings_frame, width=30, justify="center")
        plugboard_entry.insert(0, "bq cr di ej kw mt os px uz gh")
        plugboard_entry.grid(row=9, column=0, columnspan=10, pady=(0, 10))


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
        size_combobox.bind("<<ComboboxSelected>>", lambda event: generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals))
        entry_vals["size_combobox"] = size_combobox
        reset_button = ttk.Button(matrix_settings_frame, text = "Resetare alfabet", command = lambda: reset_polybius_bifid_entry(entry_vals, size_combobox))
        reset_button.grid(row = 0, column = 10, columnspan = 5)
        generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals)

    elif selected_algorithm == "Bifid Cipher":

        matrix_settings_frame = tk.Frame(settings_frame)
        matrix_settings_frame.grid(row = 0, column = 0, columnspan = 10)

        size_combobox = ttk.Combobox(matrix_settings_frame, values = ["5x5", "6x6", "7x7"], state = "readonly", width = 3)
        size_combobox.set("5x5")
        size_combobox.grid(row = 0, column = 0, columnspan = 5)
        size_combobox.bind("<<ComboboxSelected>>", lambda event: generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals))
        entry_vals["size_combobox"] = size_combobox
        reset_button = ttk.Button(matrix_settings_frame, text = "Resetare alfabet", command = lambda: reset_polybius_bifid_entry(entry_vals, size_combobox))
        reset_button.grid(row = 0, column = 10, columnspan = 5)
        generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals)

    elif selected_algorithm == "ADFGVX":

        matrix_settings_frame = tk.Frame(settings_frame)
        matrix_settings_frame.grid(row = 0, column = 0, columnspan = 10)

        size_combobox = ttk.Combobox(matrix_settings_frame, values = ["5x5", "6x6", "7x7"], state = "readonly", width = 3)
        size_combobox.set("5x5")
        size_combobox.grid(row = 0, column = 0, columnspan = 5)
        size_combobox.bind("<<ComboboxSelected>>", lambda event: generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals))
        entry_vals["size_combobox"] = size_combobox
        reset_button = ttk.Button(matrix_settings_frame, text = "Resetare alfabet", command = lambda: reset_polybius_bifid_entry(entry_vals, size_combobox))
        reset_button.grid(row = 0, column = 10, columnspan = 5)

        generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals)

        adfgvx_textbox = Cw.LabeledTextbox(settings_frame, "Cheie:","n", 1, 15, 1,0,1,10)
        entry_vals["adfgvx_textbox"] = adfgvx_textbox

    elif selected_algorithm == "Hashing":

        hashing_label = tk.Label(settings_frame, text="Alege algoritmul:")
        hashing_label.grid(row=0, column=0, columnspan = 3, sticky="w")

        hashing_choice = tk.StringVar(value="SHA-1")
        sha1_radiobutton = ttk.Radiobutton(settings_frame, text = "SHA-1", variable = hashing_choice, value = "SHA-1")
        sha1_radiobutton.grid(row = 1, column = 1, sticky = "w")
        sha256_radiobutton = ttk.Radiobutton(settings_frame, text = "SHA-256", variable = hashing_choice, value = "SHA-256")
        sha256_radiobutton.grid(row = 2, column = 1, sticky = "w")
        sha512_radiobutton = ttk.Radiobutton(settings_frame, text = "SHA-512", variable = hashing_choice, value = "SHA-512")
        sha512_radiobutton.grid(row=3, column=1, sticky="w")
        md5_radiobutton = ttk.Radiobutton(settings_frame, text = "MD5", variable = hashing_choice, value = "MD5")
        md5_radiobutton.grid(row=4, column=1, sticky="w")

        entry_vals["hashing_choice"] = hashing_choice

    elif selected_algorithm == "AES":

        aes_combobox = ttk.Combobox(settings_frame, values=["AES-128", "AES-256"], state="readonly", width=9)
        aes_combobox.set("AES-128")
        aes_combobox.grid(row=0, column=0, columnspan=5)
        aes_textbox = Cw.LabeledTextbox(settings_frame, "Cheie de criptare:", "n", 3, 15, 1, 0, 1, 1)
        entry_vals["aes_combobox"] = aes_combobox
        entry_vals["aes_textbox"] = aes_textbox

    elif selected_algorithm == "RC4":

        rc4_textbox = Cw.LabeledTextbox(settings_frame, "Cheie de criptare:", "n", 3, 15, 0, 0, 1, 1)
        entry_vals["rc4_textbox"] = rc4_textbox

    elif selected_algorithm == "Playfair Cipher":

        playfair_textbox = Cw.LabeledTextbox(settings_frame, "Cheie de criptare:", "n", 3, 15, 0, 0, 1, 1)
        entry_vals["rc4_playfair"] = playfair_textbox

    elif selected_algorithm == "Hill Cipher":

        matrix_settings_frame = tk.Frame(settings_frame)
        matrix_settings_frame.grid(row=0, column=0, columnspan=10)

        size_combobox = ttk.Combobox(matrix_settings_frame, values=["2x2", "3x3"], state="readonly", width=3)
        size_combobox.set("2x2")
        size_combobox.grid(row = 0, column = 0, columnspan = 5)
        size_combobox.bind("<<ComboboxSelected>>",lambda event: generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals))
        entry_vals["size_combobox"] = size_combobox

        generate_polybius_bifid_matrix(settings_frame, size_combobox, combobox, entry_vals)

    elif selected_algorithm == "Enigma":

        enigma_settings_frame = tk.Frame(settings_frame)
        enigma_settings_frame.grid(row=0, column=0, columnspan=10)

        enigma_version_combobox = ttk.Combobox(enigma_settings_frame, values = ["Enigma I", "Enigma M3", 'Enigma M4 "Shark"'], width = 16, state="readonly")
        enigma_version_combobox.set("Enigma I")
        enigma_version_combobox.grid(row = 0, column = 0, columnspan = 10)
        entry_vals["enigma_version_combobox"] = enigma_version_combobox
        enigma_version_combobox.bind("<<ComboboxSelected>>",lambda event: generate_enigma_options(settings_frame, enigma_version_combobox, entry_vals))

        generate_enigma_options(settings_frame, enigma_version_combobox, entry_vals)

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

def polybius_bifid_adfgvx_alphabet(entry_vals):

    alphabet = ""
    for entry in entry_vals["matrix_entry"]:
        value = entry.get()
        if value == "":
            alphabet += "  "
        else:
            alphabet += value
    return alphabet

def verify_duplicate_values(entry_vals):

    duplicate_values = set()

    for entry in entry_vals["matrix_entry"]:
        value = entry.get()
        if value in duplicate_values:
            return "Matricea conține caractere duplicate!"
        duplicate_values.add(value)

def undefined_characters(input_text, alphabet):

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

def verify_polybius_decrypt(input_text, entry_vals):

    size_combobox = entry_vals["size_combobox"].get()
    digits_text = input_text.replace(" ", "")

    for char in input_text:
        if not(char.isdigit() or char.isspace()):
            return "Mesajul trebuie să conțină doar cifre și spații!"

    if len(digits_text) % 2 != 0:
        return "Mesajul trebuie să conțină un număr par de cifre!"

    if size_combobox == "5x5":
        for digit in digits_text:
            if int(digit) < 0 or int(digit) > 4:
                return "Cifrele trebuie să fie cuprinse între 0 și 4!"

    if size_combobox == "6x6":
        for digit in digits_text:
            if int(digit) < 0 or int(digit) > 5:
                return "Cifrele trebuie să fie cuprinse între 0 și 5!"

    if size_combobox == "7x7":
        for digit in digits_text:
            if int(digit) < 0 or int(digit) > 6:
                return "Cifrele trebuie să fie cuprinse între 0 și 6!"

def verify_adfgvx_crypt(input_text, alphabet, key):

    ok = False
    for char in alphabet:
        if char == " ":
            ok = True

    if ok:
        if len(input_text) < len(key) // 2:
            return "Lungimea mesajului (cu spații) trebuie să fie cel puțin jumătate din lungimea cheii!"
    else:
        input_text = input_text.replace(" ","")
        if len(input_text) < len(key) // 2:
            return "Lungimea mesajului (fără spații) trebuie să fie cel puțin jumătate din lungimea cheii!"

def verify_adfgvx_decrypt(input_text, key):

    adfgvx_decrypt_list = ["a", "d", "f", "g", "v", "x", "z", " "]
    for char in input_text:
        if char not in adfgvx_decrypt_list:
            return "Mesajul poate fi format doar din {'A', 'D', 'F', 'G', 'V', 'X', 'Z'} și spații!"

    input_text_words = input_text.split()
    if len(input_text_words) != len(key):
        return "Numărul de cuvinte din mesaj trebuie să fie egal cu lungimea cheii!"

def crypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")
    cleaned_text = input_text.replace("\n", " ")
    cleaned_text = cleaned_text.replace("\t", " ")
    textbox2.config(state = NORMAL)
    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":
        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text(cleaned_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return

        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Basic.cezar(cleaned_text, shift_value, 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Vigenère Cipher":
        key_value = entry_vals["vigenere_textbox"].get("1.0", "end-1c")
        if not verify_textbox_vigenere(key_value):
            msgbox.showerror("Eroare", "Cheia trebuie să conțină doar litere mari sau mici! (fără spații)")
            return
        if not verify_text(cleaned_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Basic.vignere(cleaned_text, key_value, 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Polybius":
        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = undefined_characters(cleaned_text, alphabet)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.polybius(mesaj = cleaned_text, alfabet = alphabet, operatie = 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Bifid Cipher":

        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = undefined_characters(cleaned_text, alphabet)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.bifid(cleaned_text, alphabet, 'criptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "ADFGVX":
        key = entry_vals["adfgvx_textbox"].get("1.0", "end-1c")
        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = undefined_characters(cleaned_text, alphabet)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = verify_adfgvx_crypt(cleaned_text, alphabet, key)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.adfgvx(cleaned_text, alphabet, key, "criptare"))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Hashing":

        choice = entry_vals["hashing_choice"].get()

        if choice == "SHA-1":

            textbox2.delete("1.0", "end-1c")
            textbox2.insert("end-1c", Hashing.sha_1(input_text))
            textbox2.config(state = DISABLED)

        if choice == "SHA-256":

            textbox2.delete("1.0", "end-1c")
            textbox2.insert("end-1c", Hashing.sha_256(input_text))
            textbox2.config(state = DISABLED)

        if choice == "SHA-512":

            textbox2.delete("1.0", "end-1c")
            textbox2.insert("end-1c", "SHA-512")
            textbox2.config(state = DISABLED)

        if choice == "MD5":

            textbox2.delete("1.0", "end-1c")
            textbox2.insert("end-1c", "MD5")
            textbox2.config(state = DISABLED)

    elif selected_algorithm == "AES":
        ...

    elif selected_algorithm == "RC4":
        ...

def decrypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")
    cleaned_text = input_text.replace("\n", " ")
    cleaned_text = cleaned_text.replace("\t", " ")
    textbox2.config(state = NORMAL)

    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":

        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text(cleaned_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Basic.cezar(cleaned_text, shift_value, 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Vigenère Cipher":

        key_value = entry_vals["vigenere_textbox"].get("1.0", "end-1c")
        if not verify_textbox_vigenere(key_value):
            msgbox.showerror("Eroare", "Cheia trebuie să conțină doar litere mari sau mici! (fără spații)")
            return
        if not verify_text(cleaned_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Basic.vignere(cleaned_text, key_value, 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Polybius":

        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = verify_polybius_decrypt(cleaned_text, entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.polybius(mesaj = cleaned_text, alfabet = alphabet, operatie = 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Bifid Cipher":

        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.bifid(cleaned_text, alphabet, 'decriptare'))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "ADFGVX":
        key = entry_vals["adfgvx_textbox"].get("1.0", "end-1c")
        alphabet = polybius_bifid_adfgvx_alphabet(entry_vals)
        error = verify_duplicate_values(entry_vals)
        if error:
            msgbox.showerror("Eroare", error)
            return
        error = verify_adfgvx_decrypt(cleaned_text, key)
        if error:
            msgbox.showerror("Eroare", error)
            return
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", Polybius.adfgvx(cleaned_text, alphabet, key, "decriptare"))
        textbox2.config(state = DISABLED)

    elif selected_algorithm == "Hashing":

        msgbox.showerror("Eroare", "Nu există decriptare pentru algoritmii de hashing!")
        return

    elif selected_algorithm == "AES":
        ...

    elif selected_algorithm == "RC4":
        ...

def brute_force_caesar(textbox1, textbox2):

    input_text = textbox1.get("1.0", "end-1c")
    cleaned_text = input_text.replace("\n", " ")
    cleaned_text = cleaned_text.replace("\t", " ")
    textbox2.config(state = NORMAL)

    if not verify_text(cleaned_text):
        msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
        return
    string_list = Basic.cezar(cleaned_text, None, 'spargere')
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

    combobox = ttk.Combobox(options_frame, values = ["Caesar Cipher","Vigenère Cipher", "Polybius", "Bifid Cipher", "ADFGVX", "Hashing", "AES", "RC4", "Playfair Cipher", "Hill Cipher", "Enigma"], state = "readonly")
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