import tkinter as tk

from tkinter import ttk

FONT = ("Consolas", 11)

root = tk.Tk()
root.geometry("864x576")
root.title("KursCal")

#style = ttk.Style(root)
#style.theme_use("clam")

# frame containing editor
textf = ttk.Frame(root, width=640, height=500)
_ = textf.pack_propagate(False)
textf.grid(row=0, column=0, padx=5, pady=5)

# editor
vtext = tk.Text(textf, wrap="none", font=FONT, blockcursor=True, highlightthickness=0)
## vtext.insert("0.0", "uh completely normal\n\n \ne\ntest text \n    very normal fr trust me  \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n a  b")
vtext.insert("1.0", "1 1 + 3 4 * **\n1 +")
vtext.mark_set("insert", "1.0")
vtext.see("insert")
vtext.focus_set()
vtext.pack(fill="both", expand=True)

# info bar at bottom
ind = ttk.Label(root, text="INSERT", justify="left", anchor="w", font=FONT)
ind.grid(row=1, column=0, sticky="w", padx=5, pady=2)

# chars pressed
chars = ttk.Label(root, text="", justify="right", anchor="e", font=FONT)
chars.grid(row=1, column=0, sticky="e", padx=5, pady=2)

# stack frame
stackf = ttk.Frame(root, width=200, height=20)
_ = stackf.pack_propagate(False)
stackf.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# display of stack
stack_display = tk.Text(stackf, wrap="none", font=FONT, highlightthickness=0)
stack_display.configure(state="disabled")
stack_display.pack(fill="both", expand=True)

# box for error messages 
errorbox = ttk.Entry(root, font=FONT)
errorbox.insert(0, "")
errorbox.configure(state="readonly")
errorbox.configure(foreground="black")
errorbox.grid(row=2, column=0, columnspan=2, sticky="we", padx=2, pady=2)