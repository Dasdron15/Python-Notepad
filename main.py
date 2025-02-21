import tkinter as tk
from tkinter import messagebox, filedialog
import os
import ctypes
from platform import system


class Notepad:
    def __init__(self, root):
        self.root = root
        self.text_size = 25
        self.file_path = None
        self.need_save = False

        self.root.title("Untitled - Notepad")
        self.root.geometry("700x500")

        if system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.text_area = tk.Text(root, font=("Arial", self.text_size))
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<KeyPress>", self.on_key_press)
        self.text_area.bind("<KeyRelease>", self.on_key_release)

        self.create_menu()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def new_file(self):
        if self.need_save and not self.confirm_discard_changes():
            return
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Notepad")
        self.need_save = False

    def open_file(self):
        if self.need_save and not self.confirm_discard_changes():
            return
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.file_path = file_path
            self.root.title(f"{os.path.basename(file_path)} - Notepad")
            self.need_save = False

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.need_save = False
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            self.file_path = file_path
            self.save_file()
            self.root.title(f"{os.path.basename(file_path)} - Notepad")

    def on_closing(self):
        if self.need_save:
            if not self.confirm_discard_changes():
                return
        self.root.destroy()

    def confirm_discard_changes(self):
        return messagebox.askyesno(
            "Unsaved changes", "You have unsaved changes. Do you want to discard them?"
        )

    def on_key_press(self, event):
        print(event.keysym)
        self.need_save = True
        if event.state & 4 and event.keysym in {"s", "S"}:
            self.save_file()
        if event.state & 4 and event.keysym in {"equal", "plus", "+", "="}:
            self.text_size = min(self.text_size + 5, 100)
            self.text_area.config(font=("Arial", self.text_size))
        if event.state & 4 and event.keysym in {"minus", "-"}:
            self.text_size = max(10, self.text_size - 5)
            self.text_area.config(font=("Arial", self.text_size))

    def on_key_release(self, event):
        return


if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
