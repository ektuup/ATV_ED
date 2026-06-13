
from PySide6.QtWidgets import QApplication
from interface import MainWindow
import sys

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()