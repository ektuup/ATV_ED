from PySide6.QtWidgets import QApplication
from interface import MainWindow
import sys, os

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()

if os.path.exists('bst_output'):
    os.remove('bst_output') 
if os.path.exists('bst_output.png'):
    os.remove('bst_output.png')
