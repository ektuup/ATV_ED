from  PySide6 import QtWidgets, QtCore
from sortlib import SortVector
import sys, random, csv, time, os

array = SortVector()
unordened_array = SortVector()

map_sort = {
    "Bubblesort" : array.bubble_sort,
    "Selectionsort" : array.selection_sort,
    "Insertionsort" : array.insertion_sort,
    "Shellsort" : array.shell_sort,
    "Quicksort" : array.quick_sort,
    "Mergesort-Híbrido" : array.hibrid_merge_sort,
    "Mergesort-BottomUp" : array.merge_sort,
    "Heapsort" : array.heap_sort
}

def fwrite(name):
    with open(name, 'w') as f:
        for i in range(array.len()):
            f.write(array.at(i) + '\n')

def csv_write(file_name, header, sidebar, data):
    header = header
    exists = os.path.exists("estatisticas_ordenacao.csv");
    with open("estatisticas_ordenacao.csv", 'a') as fcsv:
        scanner = csv.writer(fcsv)
        if not exists:
            scanner.writerow(header)
        for nametxt in sidebar:
            scanner.writerow([nametxt] + data)

class SortWorker(QtCore.QThread):
    progress = QtCore.Signal(str)
    finished = QtCore.Signal(list)

    def __init__(self, selected_algorithms, nometxt):
        super().__init__()
        self.selected_algorithms = selected_algorithms
        self.nometxt = nometxt

    def run(self):
        times_sorts = []
        for algorithm, sort in map_sort.items():
            array.copy(unordened_array)
            if algorithm in self.selected_algorithms:
                print(algorithm)
                self.progress.emit(f"Ordenando '{self.nometxt}' com {algorithm}...")
                start = time.time()
                sort()
                end = time.time()
                times_sorts.append((end - start) * 1000)
            else:
                times_sorts.append(None)
        self.finished.emit(times_sorts)

class myButton(QtWidgets.QPushButton):
    def __init__(self, name:str, w, h, clicked = None):
        super().__init__()
        self.setText(name)
        self.setFixedSize(w, h)
        if clicked:
            self.clicked.connect(clicked)

class myWidget(QtWidgets.QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.define_data()
        self.resize(w, h)
        self.setWindowTitle("Estatísticas de Ordenação")

        self.file_button = myButton("Selecionar Arquivo", 200, 30, self.choice_file)
        self.sort_button = myButton("Métodos de Ordenação", 200, 30, self.choice_group)
        self.show_graph = myButton("Mostrar Gráfico", 200, 30)

        self.grid = QtWidgets.QGridLayout(self)
        self.grid.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.setSpacing(40)

        self.label = QtWidgets.QLabel("")
        
        self.grid.addWidget(self.file_button, 0, 0, 1, 2, QtCore.Qt.AlignCenter)                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        self.grid.addWidget(self.sort_button, 1, 0, 1, 2, QtCore.Qt.AlignCenter)                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        self.grid.addWidget(self.show_graph, 2, 0, 1, 2, QtCore.Qt.AlignCenter)                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        self.grid.addWidget(self.label, 3, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.define_styles()

    def define_data(self):
        self.squares = ["Bubblesort", "Selectionsort", "Insertionsort"]
        self.linearithmics = ["Shellsort", "Mergesort-BottomUp", "Quicksort", "Heapsort", "Mergesort-Híbrido"]
        self.files = ["nomes100k.txt", "nomes250k.txt", "nomes500k.txt", "nomes1m.txt"]
        self.groups = [
            "Bubblesort x Selection x Insertion", 
            "Shellsort x Mergesort x Quicksort x Heapsort"
        ]

        self.selected_files = []
        self.selected_algorithms = []

    def checkbox_file(self):
        dialog = CheckBoxWindow("Seleção", self.files, self)
        dialog.resize(400, 100)

        if dialog.exec():
            choices = dialog.get_results()
            self.label.setText("")

            print(f"o usuario escolheu: {choices}")
            
        return choices

    def dialog_groups(self):
        grp, ok = QtWidgets.QInputDialog.getItem(
            self,
            "seleção",
            "escolha um grupo",
            self.groups,
            0,
            False
        )
        if not ok:
            return

        if grp == self.groups[0]:
            return self.choice_squares()
        elif grp == self.groups[1]:
            return self.choice_linearithmics()

    def choice_file(self):
        self.selected_files = self.checkbox_file()
        not_exists = [s for s in self.selected_files if not os.path.exists(s)]
        
        if len(not_exists):
            self.label.setText(f"Arquivo(s) {not_exists} não encontrado(s) no diretório atual")
        
        self.selected_files = [x for x in self.selected_files if x not in not_exists]

    def choice_group(self):
        if(len(self.selected_files) == 0):
            self.label.setText("Selecione um arquivo antes de executar a ordenação!")
            return

        self.selected_algorithms = self.dialog_groups()
        self._file_queue = list(self.selected_files)
        self._run_next_file()

    def _run_next_file(self):
        if not self._file_queue:
            return

        nometxt = self._file_queue.pop(0)
        try:
            with open(nometxt, 'r') as f:
                for line in f:
                    unordened_array.insert(line.strip())
        except FileNotFoundError:
            self.label.setText(f"Arquivo '{nometxt}' não encontrado no diretório atual")
            return

        self._current_file = nometxt
        self.worker = SortWorker(self.selected_algorithms, nometxt)
        self.worker.progress.connect(self.label.setText)
        self.worker.finished.connect(self._on_sort_finished)
        self.worker.start()

    def _on_sort_finished(self, times_sorts):
        nometxt = self._current_file
        self.label.setText("Ordenação concluída!")

        nometxt_ordened = nometxt[:-4] + "_ordened.txt"
        fwrite(nometxt_ordened)

        header = ["Arquivo"] + self.squares + self.linearithmics
        sidebar = [s for s in self.selected_files]
        csv_write("estatisticas_ordenacao.csv", header, sidebar, times_sorts)

        self._run_next_file()

    def choice_linearithmics(self):
        dialog = CheckBoxWindow("Algoritmos O(nlog(n))", self.linearithmics, self)
        dialog.resize(400, 100)
        choices = None
        if dialog.exec(): 
            choices = dialog.get_results()
            print(f"selected: {choices}")
        return choices
    
    def choice_squares(self):
        dialog = CheckBoxWindow("Algoritmos O(n^2)", self.squares, self)
        dialog.resize(400, 100)
        if dialog.exec(): 
            choices = dialog.get_results()
            print(f"selected: {choices}")
        return choices

    def define_styles(self):
        self.setStyleSheet("""
            QWidget{
                background-color: #313131;
            }
            QPushButton{
                background-color: #800080;
                color: white;
                font-weight: bold;
                padding-left: 10px;
            }  
            QLabel{
                color: white;
                font-size: 16px;
            }
                           
            QCheckBox{
                color: white;
                background-color: transparent;
            }
            QCheckBox::indicator{
                border: 2px solid #fdfdfd;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked{
               background-color: #800080
            }
                           
            QInputDialog{
                background-color: #313131;
            }
            QInputDialog QComboBox {
                color: white; 
                background-color: #454545;
                selection-background-color: #800080;
            }
            QInputDialog QAbstractItemView {
                color: white;
                background-color: #313131;
                selection-background-color: #800080;
        }
        """)

class CheckBoxWindow(QtWidgets.QDialog):
    def __init__(self, title, itens, parent):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QtWidgets.QVBoxLayout(self)
        
        self.label = QtWidgets.QLabel("Selecione os métodos para comparação")
        layout.addWidget(self.label)

        self.checkboxes = []
        for item in itens:
            cb = QtWidgets.QCheckBox(item)
            layout.addWidget(cb)
            self.checkboxes.append(cb)

        self.buttons = QtWidgets.QDialogButtonBox()

        # Adiciona à caixa dizendo qual a "função" de cada um (Accept ou Reject)
        self.buttons.addButton(QtWidgets.QDialogButtonBox.Ok)
        self.buttons.addButton(QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
    
    def get_results(self):
        checked = []
        for cb in self.checkboxes:
            if cb.isChecked():
                checked.append(cb.text())
        return checked
