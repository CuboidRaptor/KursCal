import subprocess
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

mode = "i"

root = ctk.CTk()
root.geometry("720x480")
root.title("KursCal")

vtext = ctk.CTkTextbox(root, width=540, height=440, wrap="none")
vtext.grid()
vtext.focus_set()


def key_press(event):
    global mode
    key = event.char
    print(key)
    
    if mode == "n":
        return "break"

vtext.bind("<Key>", key_press)

root.mainloop()