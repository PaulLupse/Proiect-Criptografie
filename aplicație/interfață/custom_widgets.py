import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext

class LabeledTextbox(scrolledtext.ScrolledText):
    def __init__(self, master, label_text, label_position, textbox_height, textbox_width, frame_row, frame_column, rowspan, columnspan):

        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame, text = label_text)
        self.frame.grid(row = frame_row, column = frame_column, rowspan = rowspan, columnspan = columnspan, padx = 10, pady = 10)
        super().__init__(self.frame, height=textbox_height, width=textbox_width, wrap = "word")

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

class LabeledEntry(tk.Entry):
    def __init__(self, master, label_text, label_position, entry_width, frame_row, frame_column):

        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame, text = label_text)
        self.frame.grid(row = frame_row, column = frame_column, padx = 10, pady = 10)
        super().__init__(self.frame, width = entry_width, justify = "center")

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