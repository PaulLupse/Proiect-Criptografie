import tkinter as tk
from tkinter import scrolledtext

# Clasa care creeaza un ScrolledText (caseta de text cu scrollbar) cu o eticheta
class LabeledTextbox(scrolledtext.ScrolledText):
    def __init__(self, master, label_text, label_position, textbox_height, textbox_width, frame_row, frame_column, rowspan, columnspan):

        # Creeaza un frame in care punem label-ul si textbox-ul
        self.frame = tk.Frame(master)

        # Creeaza un label cu textul specificat
        self.label = tk.Label(self.frame, text = label_text)

        # Plaseaza frame-ul in fereastra principala folosind grid
        self.frame.grid(row = frame_row, column = frame_column, rowspan = rowspan, columnspan = columnspan, padx = 10, pady = 10)

        # Creeaza caseta de text cu scrollbar cu dimensiunile dorite
        super().__init__(self.frame, height=textbox_height, width=textbox_width, wrap = "word")

        # Pozitioneaza label-ul fata de textbox, in functie de label_position
        if label_position == 'n':
            self.label.grid(row = 0, column = 0)
            self.grid(row = 1, column = 0)
        if label_position == 's':
            self.label.grid(row = 1, column = 0)
            self.grid(row = 0, column = 0)
        if label_position == 'w':
            self.label.grid(row = 0, column = 0)
            self.grid(row = 0, column = 1)
        if label_position == 'e':
            self.label.grid(row = 0, column = 1)
            self.grid(row = 0, column = 0)

# Clasa care creeaza un Entry cu o eticheta
class LabeledEntry(tk.Entry):
    def __init__(self, master, label_text, label_position, entry_width, frame_row, frame_column):

        # Creeaza un frame in care punem label-ul si entry-ul
        self.frame = tk.Frame(master)

        # Creeaza un label cu textul specificat
        self.label = tk.Label(self.frame, text = label_text)

        # Plaseaza frame-ul in fereastra principala folosind grid
        self.frame.grid(row = frame_row, column = frame_column, padx = 10, pady = 10)

        # Creeaza entry-ul cu setarile dorite
        super().__init__(self.frame, width = entry_width, justify = "center")

        # Pozitioneaza label-ul fata de entry, in functie de label_position
        if label_position == 'n':
            self.label.grid(row = 0, column = 0)
            self.grid(row = 1, column = 0)
        if label_position == 's':
            self.label.grid(row = 1, column = 0)
            self.grid(row = 0, column = 0)
        if label_position == 'w':
            self.label.grid(row = 0, column = 0)
            self.grid(row = 0, column = 1)
        if label_position == 'e':
            self.label.grid(row = 0, column = 1)
            self.grid(row = 0, column = 0)