import tkinter as tk
from tkinter import messagebox, filedialog, INSERT
import os
import ctypes
from platform import system

# Variables
text_size = 25
keys_pressed = set()
can_save = False

# Functions
def on_key_press(event):
    global text_size, keys_pressed, can_save
    can_save = True
    keys_pressed.add(event.keysym)

    if "Meta_L" in keys_pressed and "=" in keys_pressed:
        text_size = min(text_size + 5, 100)
        window_base.config(font=("Arial", text_size))
    if "Meta_L" in keys_pressed and "-" in keys_pressed:
        text_size = max(10, text_size - 5)
        window_base.config(font=("Arial", text_size))

def on_key_release(event):
    global keys_pressed
    try:
        keys_pressed.remove(event.keysym)
    except:
        pass

def file_save():
    text = window_base.get(1.0, "end-1c")
    file = filedialog.asksaveasfilename(initialdir="Documents", title="Save file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file:
        with open(file, "w") as f:
            f.write(text)

def open_file():
    global window_base
    file_path = filedialog.askopenfilename(initialdir="Documents", title="Open file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            window_base.delete(1.0, "end")
            window_base.insert(INSERT, text)
            file_name = os.path.basename(file_path)
            title = f"{file_name} - Notepad"
            root.title(title)


def on_closing():
    text = window_base.get(1.0, "end-1c")
    if text != "" or can_save:
        if_save = messagebox.askquestion("Save", "Do you want to save this file?")
        if if_save == "yes":
            file_save()

    root.destroy()


def delete_text():
    text = window_base.get(1.0, "end-1c")
    if text == "":
        pass
    else:
        if_save = messagebox.askquestion("Save", "Do you want to save this file?")
        if if_save == "yes":
            file_save()
            window_base.delete(1.0, "end")
        elif if_save == "no":
            window_base.delete(1.0, "end")

# Window settings
title = "Notepad"
root = tk.Tk()
root.geometry("700x500")
root.title(title)

if system() == "Windows":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Area where you type your text
window_base = tk.Text(root, height=300, width=500, font=("Arial", text_size))
window_base.pack()

# Keybinds
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Create menubar
menubar = tk.Menu()

# Menu Bar settings
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="New file", command=delete_text)
file.add_command(label="Open...", command=open_file)
file.add_command(label="Save as...", command=file_save)
file.add_separator()
file.add_command(label="Quit", command=root.destroy)

# Detecting when the window is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

root.config(menu=menubar)
root.mainloop()