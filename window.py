import tomllib

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit

with open("./config.toml", "rb") as f:
    CONFIG = tomllib.load(f)
    COLORS = CONFIG["theme"]["colors"]
    FONT = (CONFIG["theme"]["font"]["font"], CONFIG["theme"]["font"]["fontsize"])

app = QApplication([])

window = QWidget()
window.setWindowTitle("KursCal")
window.resize(864, 576)
window.setStyleSheet(f"background-color: {COLORS['bg']};")
window.setAutoFillBackground(True)

font = QFont(*FONT)
app.setFont(font, "QPlainTextEdit")

vtext = QPlainTextEdit(window)
vtext.resize(640, 500)
vtext.setStyleSheet(f"""
margin-left: 5px;
margin-top: 5px;
color: {COLORS['fg']};
border: 2px solid {COLORS['fg']};
""")


window.show()