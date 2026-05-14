import sys
from PySide6 import QtWidgets
from interface import myWidget

app = QtWidgets.QApplication()
widget = myWidget(800, 400)
widget.show()
sys.exit(app.exec())