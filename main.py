import tkinter as tk
from tkinter import messagebox, filedialog, INSERT
import os
import ctypes
from platform import system

# Variables
text_size = 25
keys_pressed = set()
need_save = False
opened_file = False

# Functions
def on_key_press(event):
    global text_size, keys_pressed, need_save, opened_file
    if opened_file and need_save:
        title = f"{file_name} - Notepad (*)"
        root.title(title)

    if window_base.get(1.0, "end-1c") != "": # Check if something was written if yes then save
        need_save = True
    keys_pressed.add(event.keysym)

    if "Meta_L" in keys_pressed and "s" in keys_pressed:
        title = f"{file_name} - Notepad"
        root.title(title)
        with open(file_path, "w") as file:
            file.write(window_base.get(1.0, "end-1c"))
        need_save = False

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
    global window_base, need_save, file_name, file_path, opened_file
    file_path = filedialog.askopenfilename(initialdir="Documents", title="Open file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    if need_save:
        on_closing(False)

    need_save = False
    opened_file = True

    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            window_base.delete(1.0, "end")
            window_base.insert(INSERT, text)
            file_name = os.path.basename(file_path)
            title = f"{file_name} - Notepad"
            root.title(title)

def on_closing(is_close=True):
    if need_save:
        if_save = messagebox.askquestion("Save", "Do you want to save this file?")
        if if_save == "yes" and not opened_file:
            file_save()
        elif if_save == "yes" and opened_file:
            with open(file_path, "w") as file:
                file.write(window_base.get(1.0, "end-1c"))
        

    if is_close:
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
title = "Untitled - Notepad"
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