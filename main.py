import window
import editor
import err
import ev
import tkinter as tk

from collections import deque
from decimal import Decimal

def calc():
    text: str = window.vtext.get("1.0", "end")
    data: deque[Decimal] | err.Error = ev.ev(text)
    if not isinstance(data, err.Error):
        window.stack_display.configure(state="normal")
        window.stack_display.delete("1.0", "end")
        window.stack_display.insert("1.0", ev.format_stack(data))
        window.stack_display.configure(state="disabled")

def keyreleased(event: tk.Event):
    modified = window.vtext.edit_modified()
    window.vtext.edit_modified(False)
    if (editor.mode == "i") and modified:
        return calc()

if __name__ == "__main__":
    _ = window.vtext.bind("<Key>", editor.keypress)
    _ = window.vtext.bind("<<Modified>>", keyreleased)
    _ = window.vtext.bind("<Control-Key-a>", editor.select_all)
    window.vtext.mark_set("temp", "1.0")
    window.root.mainloop()