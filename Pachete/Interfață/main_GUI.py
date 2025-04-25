import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import CustomWidgets as Cw

def update_settings(combobox, settings_frame, entry_vals):

    for widget in settings_frame.winfo_children():
        widget.destroy()

    selected_algorithm = combobox.get()

    if selected_algorithm == "Caesar Cipher":
        caesar_entry = Cw.LabeledEntry(settings_frame, "Cheie pentru shiftare:", "w", 4,0,0)
        caesar_entry.insert(0,"0")
        brute_force_button = ttk.Button(settings_frame, text = "Spargere parolă", width = 23, command = lambda: brute_force_caesar(entry_vals["textbox1"], entry_vals["textbox2"]))
        brute_force_button.grid(row = 1, column = 0)
        entry_vals["caesar_entry"] = caesar_entry

    elif selected_algorithm == "Enigma":
        enigma_rotor1 = Cw.LabeledEntry(settings_frame, "Rotor 1:", "w", 4,0,0)
        enigma_rotor2 = Cw.LabeledEntry(settings_frame, "Rotor 2:", "w", 4, 1, 0)
        enigma_rotor3 = Cw.LabeledEntry(settings_frame, "Rotor 3:", "w", 4, 2, 0)

def verify_text_caesar(text):

    for char in text:
        if not (char.isalpha() or char.isspace()):
            return False
    return True

def verify_entry_caesar(val):

    if val < -100 or val > 100:
        return False
    return True

def crypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")

    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":
        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text_caesar(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return
        output_text = "Test1"                # aici o sa fie egal cu stringul returnat de functie
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", output_text) #in loc de input text trebuie rezultatul functiei

def decrypt(textbox1, textbox2, combobox, entry_vals):

    selected_algorithm = combobox.get()
    input_text = textbox1.get("1.0", "end-1c")

    if selected_algorithm == "Alege algoritmul":
        msgbox.showerror("Eroare", "Selectează un algoritm de criptare!")

    elif selected_algorithm == "Caesar Cipher":
        try:
            shift_value = int(entry_vals["caesar_entry"].get())
        except ValueError:
            msgbox.showerror("Eroare", "Cheia trebuie să fie un număr întreg!")
            return
        if not verify_text_caesar(input_text):
            msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
            return
        if not verify_entry_caesar(shift_value):
            msgbox.showerror("Eroare","Cheia trebuie să fie cuprinsă între -100 și 100!")
            return
        output_text = "Test2"              #aici output_text o sa fie stringul returnat de functie
        textbox2.delete("1.0", "end-1c")
        textbox2.insert("end-1c", output_text)

def brute_force_caesar(textbox1, textbox2):

    input_text = textbox1.get("1.0", "end-1c")

    if not verify_text_caesar(input_text):
        msgbox.showerror("Eroare", "Mesajul trebuie să conțină doar litere mari sau mici!")
        return
    string_list = ["Test1", "Test2", "Test3"]    #aici string_list o sa fie egal cu lista de stringuri ce o returneaza functia
    textbox2.delete("1.0", "end-1c")
    for i, string in enumerate(string_list, start=1):
        textbox2.insert("end", f"{i}. {string}\n")


def main():

    root = tk.Tk()
    root.resizable(False,False)
    root.title("Algoritmi de Criptare")
    root.iconbitmap("imagine-lacat.ico")
    entry_vals = {}

    textbox1 = Cw.LabeledTextbox(root, "Text:", "n", 10, 20,0,0,20,1)
    entry_vals["textbox1"] = textbox1
    textbox2 = Cw.LabeledTextbox(root, "Text criptat/decriptat:", "n", 10, 20,0,2,20,1)
    entry_vals["textbox2"] = textbox2

    options_frame = tk.Frame(root)
    options_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "n")
    settings_frame = tk.Frame(root)
    settings_frame.grid(row=1, column=1, sticky="n")

    combobox = ttk.Combobox(options_frame, values=["Caesar Cipher","Enigma"], state="readonly")
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