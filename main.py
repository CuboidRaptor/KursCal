import tkinter as tk

from tkinter import ttk

FONT = ("Consolas", 11)
TEMPMARK = "temp"
vert_memory: None | int = None # allow the cursor to snap back if interrupted while moving only vertically
count: str = ""
chars_pressed: str = ""

root = tk.Tk()
root.geometry("720x480")
root.title("KursCal")

# frame containing editor
textf = ttk.Frame(root, width=540, height=440)
## textf.columnconfigure(0, weight=10)
_ = textf.pack_propagate(False)
textf.grid(row=0, column=1)

# editor
vtext = tk.Text(textf, wrap="none", font=FONT, blockcursor=True)
vtext.insert("0.0", "uh completely normal\n\n \ne\ntest text \n    very normal fr trust me  \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n a  b")
vtext.pack(fill="both", expand=True)
vtext.mark_set("insert", "0.0")
vtext.see("insert")
vtext.focus_set()

# info bar at bottom
ind = ttk.Label(root, text="INSERT", justify="left", anchor="w", font=FONT)
ind.grid(row=1, column=1, sticky="w")

# chars pressed
chars = ttk.Label(root, text="", justify="right", anchor="e", font=FONT)
chars.grid(row=1, column=1, sticky="e")

mode = ""

def modeset(m: str):
    global mode
    if m == "n":
        _ = ind.configure(text="NORMAL")
        _ = vtext.configure(blockcursor=True)
        _ = vtext.configure(insertbackground="gray")

    elif m == "i":
        _ = ind.configure(text="INSERT")
        _ = vtext.configure(blockcursor=False)
        _ = vtext.configure(insertbackground="black")

    mode = m

modeset("i")

class Mark:
    def __init__(self, pos: str | int, pos2: str | int | None=None, nocheck:bool=False):
        self.pair: list[int]

        if pos2 is None: # set mark and then read it to resolve things like end, end-1c, etc.
            vtext.mark_set(TEMPMARK, pos)
            self.pair = [int(i) for i in vtext.index(TEMPMARK).split(".")]

        else: # also resolve so we can use "end" in list pairs
            tempstr: str = ".".join([str(i) for i in (pos, pos2)])
            vtext.mark_set(TEMPMARK, tempstr)
            self.pair = [int(i) for i in vtext.index(TEMPMARK).split(".")]

        if not nocheck:
            self.check_bounds()

    def check_bounds(self) -> None:
        endline = Mark("end", nocheck=True).pair[0] # nocheck=True otherwise the _.end mark gets checked and we start an infintie recursive loop :skull:
        if self.pair[0] >= endline: # vertical/bottom
            self.pair[0] = endline - 1

        elif self.pair[0] <= 0: # vertical/top
            self.pair[0] = 1

        cur_line_end = Mark(self.pair[0], "end", nocheck=True).pair[1]
        if (self.pair[1] >= cur_line_end) and (mode == "n"): # horizontal/right
            self.pair[1] = cur_line_end - 1

        if self.pair[1] < 0:
            self.pair[1] = 0

    def string(self):
        return ".".join([str(i) for i in self.pair])

    def setvalue(self, ind: int, val: int) -> None:
        self.pair[ind] = val
        self.check_bounds()

    def changevalue(self, ind: int, val: int) -> None:
        self.pair[ind] += val
        self.check_bounds()

def getcursor() -> Mark:
    return Mark(vtext.index("insert"))

def setcursor(cursor: Mark) -> None: # set cursor tuple OR mark
    vtext.mark_set("insert", cursor.string())
    vtext.see("insert")

def movecursor(amount: tuple[int, int]) -> None:
    cursor = getcursor()
    cursor.changevalue(0, amount[0])
    cursor.changevalue(1, amount[1])
    setcursor(cursor)

def get_line_end(line: int) -> int:
    return Mark(line, "end").pair[1]

keydict = {
    "h": "Left",
    "j": "Down",
    "k": "Up",
    "l": "Right"
}
def arrowmove(d: str):
    global vert_memory, count
    ct = int(count) if count != "" else 1
    if d == "Left":
        movecursor((0, -ct))
        vert_memory = None

    elif d == "Down":
        if vert_memory is None:
            vert_memory = getcursor().pair[1]

        cursor = getcursor() 
        cursor.changevalue(0, ct)
        cursor.setvalue(1, vert_memory)
        setcursor(cursor)

    elif d == "Up":
        if vert_memory is None:
            vert_memory = getcursor().pair[1]

        cursor = getcursor()
        cursor.changevalue(0, -ct)
        cursor.setvalue(1, vert_memory)
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
allowed = set("aihjkl0123456789wbWB") # allowed chars so things like Control_L don't get displayed
# (if chars are in either allowed or chardict they are allowed to be displayed in the keypress register)
def charset(key: str) -> None:
    global chars_pressed
    char: str | None = chardict.get(key, key if key in allowed else None)

    if char is not None:
        chars_pressed += char

    else:
        print(f"char input \"{key}\" blocked")

    _ = chars.configure(text=chars_pressed[-32:])

def keypress(event: tk.Event) -> None | str:
    global vert_memory, count
    key = str(event.keysym)
    print(key)

    if mode == "i":
        if key in {"Left", "Down", "Up", "Right"}:
            arrowmove(key)
            return "break"

        if key == "Escape":
            movecursor((0, -1))
            modeset("n")

        vert_memory = None

    elif mode == "n":
        charset(key)

        if key in set("hjkl"):
            arrowmove(keydict[key])
            return "break"

        if (key in set("123456789")) or ((key == "0") and (count != "")):
            count += key
            return "break"

        elif key == "0":
            if count == "":
                cursor = getcursor()
                cursor.setvalue(1, 0)
                setcursor(cursor)

        if key == "a":
            modeset("i")
            movecursor((0, 1))

        elif key == "i":
            modeset("i")

        elif key in {"underscore", "asciicircum", "Home"}:
            cursor = getcursor()
            cursor.setvalue(1, 0)
            setcursor(cursor)

        elif key in {"dollar", "End"}:
            cursor = getcursor()
            cursor.setvalue(1, get_line_end(cursor.pair[0]))
            setcursor(cursor)

        elif key in set("Ww"):
            # yes I know this isn't consistent with nvim but it's a calculator so idc
            cursor: Mark = getcursor()
            cursorline: int = cursor.pair[0]
            line: str = vtext.get(f"{cursorline}.0", f"{cursorline}.end")
            cursorind: int = cursor.pair[1]
            last_line: int = Mark("end-1c").pair[0]

            ct = int(count) if count != "" else 1
            for _i in range(0, ct):
                fullbreak: bool = False
                line_changed: bool = False

                while True:
                    line_end = get_line_end(cursorline)
                    if (cursorind > (line_end) or ((cursorind == line_end) and (line == ""))):
                        cursorline += 1

                        if cursorline > last_line:
                            setcursor(Mark("end-1c"))
                            count = ""
                            return "break"

                        cursorind = 0
                        line = vtext.get(f"{cursorline}.0", f"{cursorline}.end")

                        if line == "":
                            cursorind = 0
                            fullbreak = True
                            break

                        line_changed = True

                    elif (line[cursorind] != " ") and not (line_changed):
                        cursorind += 1

                    else:
                        break

                if not fullbreak:
                    while True:
                        if cursorind > (get_line_end(cursorline)):
                            cursorline += 1

                            if cursorline > last_line:
                                setcursor(Mark("end-1c"))
                                count = ""
                                return "break"

                            cursorind = 0
                            line = vtext.get(f"{cursorline}.0", f"{cursorline}.end")

                            if line == "":
                                cursorind = 0
                                fullbreak = True
                                break

                        elif (line[cursorind] == " "):
                            cursorind += 1

                        else:
                            break

            setcursor(Mark(cursorline, cursorind))

        elif key in set("Bb"):
            # yes I know this isn't consistent with nvim but it's a calculator so idc
            cursor: Mark = getcursor()
            cursorline: int = cursor.pair[0]
            line: str = vtext.get(f"{cursorline}.0", f"{cursorline}.end")
            cursorind: int = cursor.pair[1] - 1

            ct = int(count) if count != "" else 1
            for _i in range(0, ct):
                fullbreak: bool = False
                cursorind -= 1

                while True:
                    if cursorind < 0:
                        cursorline -= 1

                        if cursorline < 1:
                            setcursor(Mark(1, 0))
                            count = ""
                            return "break"

                        cursorind = get_line_end(cursorline)
                        line = vtext.get(f"{cursorline}.0", f"{cursorline}.end")

                        if line == "":
                            cursorind = 0
                            fullbreak = True
                            break

                    elif (line[cursorind] == " "): # if line wrap to previous line, don't move left again
                        cursorind -= 1

                    else:
                        break

                if not fullbreak:
                    while (cursorind >= 0) and line[cursorind] != " ": # first conditional otherwise error (I love short-circuiting)
                        cursorind -= 1
                        # don't line wrap check because characters at the start of the line implies an end to traveling

                    cursorind += 1


            setcursor(Mark(cursorline, cursorind))

        vert_memory = None
        count = ""

        return "break" # tell tk.Text to not handle input

if __name__ == "__main__":
    _ = vtext.bind("<Key>", keypress)
    vtext.mark_set("temp", "0.0")
    root.mainloop()