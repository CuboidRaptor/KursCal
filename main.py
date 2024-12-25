import window
import editor

if __name__ == "__main__":
    _ = window.vtext.bind("<Key>", editor.keypress)
    _ = window.vtext.bind("<<Modified>>", editor.keyreleased)
    _ = window.vtext.bind("<Control-Key-a>", editor.select_all)
    _ = window.vtext.bind("<Tab>", editor.tab)
    window.root.mainloop()