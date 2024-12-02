import tkinter as tk

from tkinter import ttk

font = ("Consolas", 11)
TEMPMARK = "temp"
vert_memory = None # allow the cursor to snap back if interrupted while moving only vertically
count = ""
chars_pressed = []

root = tk.Tk()
root.geometry("720x480")
root.title("KursCal")

# frame containing editor
textf = ttk.Frame(root, width=540, height=440)
textf.grid(row=0, column=1)
textf.columnconfigure(0, weight=10)
textf.grid_propagate(False)

# editor
vtext = tk.Text(textf, wrap="none", font=font, blockcursor=True)
vtext.insert("0.0", "uh completely normal\ntest text\nvery normal fr trust me")
vtext.grid(row=0, column=1)
vtext.focus_set()

# info bar at bottom
ind = ttk.Label(root, text="INSERT", justify="left", anchor="w", font=font)
ind.grid(row=1, column=1, sticky="w")

# chars pressed
chars = ttk.Label(root, text="", justify="right", anchor="e", font=font)
chars.grid(row=1, column=1, sticky="e")

mode = ""

def modeset(m):
    global mode
    if m == "n":
        ind.configure(text="NORMAL")
        vtext.configure(blockcursor=True)
        vtext.configure(insertbackground="gray")

    elif m == "i":
        ind.configure(text="INSERT")
        vtext.configure(blockcursor=False)
        vtext.configure(insertbackground="black")

    mode = m

modeset("i")

def getcursor():
    return [int(i) for i in vtext.index(tk.INSERT).split(".")]

def setcursor(cursor):
    vtext.mark_set(tk.INSERT, ".".join([str(i) for i in check_cursor_bounds(cursor)]))

def get_line_end(cursor):
    vtext.mark_set(TEMPMARK, f"{str(cursor[0])}.end") # set tempmark to line end and read value
    return int(vtext.index(TEMPMARK).split(".")[1])

def check_cursor_bounds(cursor):
    endline = int(vtext.index(tk.END).split(".")[0])
    if cursor[0] >= endline: # vertical/bottom
        cursor[0] = endline - 1

    elif cursor[0] <= 0: # vertical/top
        cursor[0] = 1

    cur_line_end = get_line_end(cursor)
    if (cursor[1] >= cur_line_end) and (mode == "n"): # horizontal/right
        cursor[1] = cur_line_end - 1

    return cursor

def movecursor(amount):
    cursor = getcursor()
    cursor[0] += amount[0]
    cursor[1] += amount[1]
    setcursor(cursor)

keydict = {
    "h": "Left",
    "j": "Down",
    "k": "Up",
    "l": "Right"
}
def arrowmove(d):
    global vert_memory, count
    ct = int(count) if count != "" else 1
    if d == "Left":
        movecursor((0, -ct))
        vert_memory = None

    elif d == "Down":
        if vert_memory is None:
            vert_memory = getcursor()[1]

        cursor = getcursor()
        cursor[0] += ct
        cursor[1] = vert_memory
        setcursor(cursor)

    elif d == "Up":
        if vert_memory is None:
            vert_memory = getcursor()[1]

        cursor = getcursor()
        cursor[0] -= ct
        cursor[1] = vert_memory
        setcursor(cursor)

    elif d == "Right":
        movecursor((0, ct))
        vert_memory = None

    count = ""

chardict = {
    "underscore": "_",
    "asciicircum": "^",
    "Home": "<Home>",
    "dollar": "$",
    "End": "<End>"
}
allowed = set("aihjkl0123456789") # allowed chars so things like Control_L don't get displayed
def charset(key):
    global chars_pressed
    char = chardict.get(key, key if key in allowed else None)
    chars_pressed.append(char) if char is not None else ...
    #chars_pressed = chars_pressed[-10:]

    chars.configure(text="".join(chars_pressed)[-32:])

def keypress(event):
    global vert_memory, count
    key = event.keysym
    print(key)

    if mode == "i":
        if key in {"Left", "Down", "Up", "Right"}:
            arrowmove(key)
            return "break"

        if key == "Escape":
            modeset("n")
            movecursor((0, -1))

        vert_memory = None

    elif mode == "n":
        charset(key)

        if key in set("hjkl"):
            arrowmove(keydict[key])
            return "break"

        if key in set("0123456789"):
            count += key
            return "break"

        if key == "a":
            modeset("i")
            movecursor((0, 1))
            charset("a")

        elif key == "i":
            modeset("i")
            charset("i")

        elif key in {"underscore", "asciicircum", "Home"}:
            cursor = getcursor()
            cursor[1] = 0
            setcursor(cursor)

        elif key in {"dollar", "End"}:
            cursor = getcursor()
            cursor[1] = get_line_end(cursor)
            setcursor(cursor)

        vert_memory = None
        count = ""

        return "break" # tell tk.Text to not handle input

if __name__ == "__main__":
    vtext.bind("<Key>", keypress)
    vtext.mark_set("temp", "0.0")
    root.mainloop()