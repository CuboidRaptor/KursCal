import tkinter as tk
import window
import err
import ev

from collections import deque
from decimal import Decimal

TEMPMARK = "temp"
vert_memory: None | int = None # allow the cursor to snap back if interrupted while moving only vertically
count = ""
chars_pressed = ""
mode = ""

colors = {
    "highlight_dark": "#888888",
    "fg": "#000000",
    "err": "#ff0000"
}

def modeset(m: str):
    global mode
    if m == "n":
        _ = window.ind.configure(text="NORMAL")
        _ = window.vtext.configure(blockcursor=True)
        _ = window.vtext.configure(insertbackground=colors["highlight_dark"])

    elif m == "i":
        _ = window.ind.configure(text="INSERT")
        _ = window.vtext.configure(blockcursor=False)
        _ = window.vtext.configure(insertbackground=colors["fg"])

    mode = m

modeset("i")

class Mark:
    def __init__(self, pos: str | int, pos2: str | int | None=None, nocheck:bool=False):
        self.pair: list[int]

        if pos2 is None: # set mark and then read it to resolve things like end, end-1c, etc.
            window.vtext.mark_set(TEMPMARK, pos)
            self.pair = [int(i) for i in window.vtext.index(TEMPMARK).split(".")]

        else: # also resolve so we can use "end" in list pairs
            tempstr = ".".join([str(i) for i in (pos, pos2)])
            window.vtext.mark_set(TEMPMARK, tempstr)
            self.pair = [int(i) for i in window.vtext.index(TEMPMARK).split(".")]

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

def bounds_check() -> None:
    # like Mark.check_cursor_bounds() but it's always on INSERT
    insert_pos = Mark(window.vtext.index("insert"))
    insert_pos.check_bounds()
    window.vtext.mark_set("insert", insert_pos.string())

def getcursor() -> Mark:
    return Mark(window.vtext.index("insert"))

def setcursor(cursor: Mark) -> None: # set cursor tuple OR mark
    window.vtext.mark_set("insert", cursor.string())
    window.vtext.see("insert")

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
def charset(key: str) -> None:
    global chars_pressed
    char: str | None = chardict.get(key, key)
    chars_pressed += char

    _ = window.chars.configure(text=chars_pressed[-32:])

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
        valid = True
        if (key in set("123456789")) or ((key == "0") and (count != "")):
                count += key

        else:
            if key in set("hjkl"):
                arrowmove(keydict[key])

            else:
                try:
                    if key == "0":
                        if count == "":
                            cursor = getcursor()
                            cursor.setvalue(1, 0)
                            setcursor(cursor)

                    elif key == "a":
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
                        cursorline = cursor.pair[0]
                        line = window.vtext.get(f"{cursorline}.0", f"{cursorline}.end")
                        cursorind = cursor.pair[1]
                        last_line = Mark("end-1c").pair[0]

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
                                        raise err.BreakExc()

                                    cursorind = 0
                                    line = window.vtext.get(f"{cursorline}.0", f"{cursorline}.end")

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
                                            raise err.BreakExc()

                                        cursorind = 0
                                        line = window.vtext.get(f"{cursorline}.0", f"{cursorline}.end")

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
                        cursorline = cursor.pair[0]
                        line = window.vtext.get(f"{cursorline}.0", f"{cursorline}.end")
                        cursorind = cursor.pair[1]

                        ct = int(count) if count != "" else 1
                        for _i in range(0, ct):
                            fullbreak: bool = False
                            cursorind -= 1

                            while True:
                                if cursorind < 0:
                                    cursorline -= 1

                                    if cursorline < 1:
                                        setcursor(Mark(1, 0))
                                        raise err.BreakExc()

                                    cursorind = get_line_end(cursorline)
                                    line = window.vtext.get(f"{cursorline}.0", f"{cursorline}.end")

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

                    elif key == "x":
                        ct = int(count) if count != "" else 1
                        for _i in range(0, ct):
                            insert_pos = Mark(window.vtext.index("insert"), nocheck=True)
                            line_end = Mark(insert_pos.pair[0], "end", nocheck=True)
                            if insert_pos.pair[1] < line_end.pair[1]:
                                window.vtext.delete(insert_pos.string())
                                bounds_check()

                        calc()

                    else:
                        # invalid key!!!!
                        valid = False
                        print(f"char input \"{key}\" blocked")

                except err.BreakExc:
                    pass

                vert_memory = None

            count = ""

        if valid:
            charset(key)

        return "break" # tell tk.Text to not handle input

def select_all(event):
    window.vtext.tag_add("sel", "1.0", "end-1c")
    window.vtext.mark_set("insert", "1.0")
    return "break"

def calc():
    text = window.vtext.get("1.0", "end")
    data: deque[Decimal] | err.Error = ev.ev(text)
    if not isinstance(data, err.Error):
        # show stack
        window.stack_display.configure(fg=colors["fg"])
        window.stack_display.configure(state="normal")
        window.stack_display.delete("1.0", "end")
        window.stack_display.insert("1.0", ev.format_stack(data))
        window.stack_display.configure(state="disabled")

        # reset errorbox
        window.errorbox.configure(state="normal")
        window.errorbox.delete(0, "end")
        window.errorbox.insert(0, "")
        window.errorbox.configure(state="readonly")

    else:
        # red stack to indicate error
        window.stack_display.configure(fg=colors["err"])

        # display error
        window.errorbox.configure(state="normal")
        window.errorbox.delete(0, "end")
        window.errorbox.insert(0, data.string)
        window.errorbox.configure(state="readonly")

def keyreleased(event: tk.Event):
    modified = window.vtext.edit_modified()
    window.vtext.edit_modified(False)
    if (mode == "i") and modified:
        return calc()

def tab(event: tk.Event):
    window.vtext.insert("insert", " " * 4)
    return "break"