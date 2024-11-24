import sys
import ev

import PySide6.QtWidgets as qw

app = qw.QApplication(sys.argv)

editbox = qw.QTextEdit("fully functional calculator fr")
editbox.show()
sys.exit(app.exec())

# nvim --clean -i "./clutter/shada/state" -u "./pnvim.lua"