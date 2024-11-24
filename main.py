import sys
from PySide6 import QtCore, QtWidgets

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start(
            "urxvt", [
                "-embed", str(int(self.winId())),
                "-e", "nvim"
            ]
        )
        self.setFixedSize(640, 480)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    term = EmbTerminal()
    term.show()
    sys.exit(app.exec())