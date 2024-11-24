import subprocess
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()
root.geometry("720x480")
termf = ctk.CTkFrame(root, height=480, width=720)

termf.pack(fill=tk.BOTH, expand=tk.YES)
wid = termf.winfo_id()
_ = subprocess.Popen(f"urxvt -embed {wid}", shell=True)

root.mainloop()