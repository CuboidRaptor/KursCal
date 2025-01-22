import tkinter as tk
import tomllib

from tkinter import ttk

with open("./config.toml", "rb") as f:
    CONFIG = tomllib.load(f)
    COLORS = CONFIG["theme"]["colors"]
    FONT = (CONFIG["theme"]["font"]["font"], CONFIG["theme"]["font"]["fontsize"])

root = tk.Tk()
root.configure(background=COLORS["bg"])
root.geometry("864x576")
root.title("KursCal")

# frame containing editor
textf = ttk.Frame(root, width=640, height=500)
_ = textf.pack_propagate(False)
textf.grid(row=0, column=0, padx=5, pady=5)

# editor
vtext = tk.Text(
    textf,
    font=FONT, fg=COLORS["fg"], bg=COLORS["bg"],
    wrap="none",
    highlightthickness=0
)
## vtext.insert("0.0", "uh completely normal\n\n \ne\ntest text \n    very normal fr trust me  \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n a  b")
vtext.insert("1.0", "1 1 + 3 4 * **\n1 +")
vtext.mark_set("insert", "1.0")
vtext.see("insert")
vtext.focus_set()
vtext.pack(fill="both", expand=True)

# info bar at bottom
ind = ttk.Label(
    root,
    text="INSERT",
    font=FONT, foreground=COLORS["fg"], background=COLORS["bg"],
    justify="left", anchor="w"
)
ind.grid(
    row=1, column=0,
    sticky="w",
    padx=5, pady=2
)

# chars pressed
chars = ttk.Label(
    root,
    text="",
    font=FONT, foreground=COLORS["fg"], background=COLORS["bg"],
    justify="right", anchor="e"
)
chars.grid(
    row=1, column=0,
    sticky="e",
    padx=5, pady=2
)

# stack frame
stackf = ttk.Frame(root, width=200, height=20)
_ = stackf.pack_propagate(False)
stackf.grid(
    row=0, column=1,
    sticky="nsew",
    padx=5, pady=5
)

# display of stack
stack_display = tk.Text(
    stackf,
    font=FONT, fg=COLORS["fg"], bg=COLORS["bg"],
    wrap="none",
    highlightthickness=0
)
stack_display.configure(state="disabled")
stack_display.pack(fill="both", expand=True)

# box for error messages 
errorbox = tk.Entry(
    root,
    font=FONT, foreground=COLORS["err"], background=COLORS["bg"], readonlybackground=COLORS["bg"],
    relief="flat",
    state="readonly",
    border=0,
    borderwidth=0
)
errorbox.grid(
    row=2, column=0, columnspan=2,
    sticky="we",
    padx=2, pady=2
)