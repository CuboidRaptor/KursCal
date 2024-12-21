import window
import editor

if __name__ == "__main__":
    _ = window.vtext.bind("<Key>", editor.keypress)
    _ = window.vtext.bind("<<Modified>>", editor.keyreleased)
    _ = window.vtext.bind("<Control-Key-a>", editor.select_all)
    window.vtext.mark_set("temp", "1.0")
    window.root.mainloop()