import sys
import ev

from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("fully functional calculator fr")
label.show()
sys.exit(app.exec())