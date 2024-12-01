import tkinter as tk

from tkinter import ttk

font = ("Consolas", 11)
tempmark = "temp"

root = tk.Tk()
root.geometry("720x480")
root.title("KursCal")

textf = ttk.Frame(root, width=540, height=440)
textf.grid(row=0, column=1)
textf.columnconfigure(0, weight=10)
textf.grid_propagate(False)

vtext = tk.Text(textf, wrap="none", font=font, blockcursor=True)
vtext.insert("0.0", "skibidi\ntoiler!")
vtext.grid(row=0, column=1)
vtext.focus_set()

ind = ttk.Label(root, text="skibidi", justify="left", anchor="w", font=font)
ind.grid(row=1, column=1, sticky="w")

mode = ""

def modeset(m):
    global mode, ind, vtext
    if m == "n":
        ind.configure(text="Normal")
        vtext.configure(blockcursor=True)
        vtext.configure(insertbackground="gray")

    elif m == "i":
        ind.configure(text="Insert")
        vtext.configure(blockcursor=False)
        vtext.configure(insertbackground="black")

    mode = m

modeset("i")

def getcursor():
    global vtext
    return [int(i) for i in vtext.index(tk.INSERT).split(".")]

def setcursor(cursor):
    global vtext
    vtext.mark_set(tk.INSERT, ".".join([str(i) for i in check_cursor_bounds(cursor)]))

def get_line_end(cursor):
    vtext.mark_set(tempmark, f"{str(cursor[0])}.end") # set tempmark to line end and read value
    return int(vtext.index(tempmark).split(".")[1])

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

def keypress(event):
    global mode
    key = event.keysym
    print(key)

    if mode == "i":
        if key == "Escape":
            modeset("n")
            movecursor((0, -1))

        elif key in {"Left", "Down", "Up", "Right"}:
            if key == "Left":
                movecursor((0, -1))

            elif key == "Down":
                movecursor((1, 0))

            elif key == "Up":
                movecursor((-1, 0))

            elif key == "Right":
                movecursor((0, 1))

            return "break"

    elif mode == "n":
        if key == "a":
            modeset("i")
            movecursor((0, 1))

        elif key == "i":
            modeset("i")

        elif key in set("hjkl"):
            cursor = getcursor()
            if key == "h":
                cursor[1] -= 1

            elif key == "j":
                cursor[0] += 1

            elif key == "k":
                cursor[0] -= 1

            elif key == "l":
                cursor[1] += 1

            setcursor(cursor)

        return "break"

if __name__ == "__main__":
    vtext.bind("<Key>", keypress)
    vtext.mark_set("temp", "0.0")
    root.mainloop()