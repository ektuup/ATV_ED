from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt, QTimer    
from PySide6.QtGui import QColor, QPixmap, QIntValidator
import numpy as np
import sys
import graphviz
from BST import bst
from my_queue import Queue
from normal import *

def fwrite(name, text):
    with open(name, 'w') as f:
        f.write(text)


def visualize_bst(bst, dot=None):
    if dot == None:
        dot = graphviz.Digraph()
        dot.attr(ordering='out')
    if bst.root == None:
        return
    
    dq = Queue()
    dq.enqueue((bst.root, 0))
    nv = 0

    while not dq.empty():
        node, nv = dq.dequeue()        
        if nv > 3:
            break

        dot.node(str(node.key), shape='circle', style='filled', fillcolor='#ffffff')

        if node.left and nv + 1 <= 3:
            dot.edge(str(node.key), str(node.left.key), color='blue')
            dq.enqueue((node.left, nv + 1))
        elif node.right:
            inv_label = f"lbl_{node.key}"
            dot.node(inv_label, style='invis')
            dot.edge(str(node.key), inv_label, style="invis")
        
        if node.right and nv + 1 <= 3:
            dq.enqueue((node.right, nv + 1))
            dot.edge(str(node.key), str(node.right.key), color='blue')
        elif node.left:
            inv_label = f"lbl_{node.key}"
            dot.node(inv_label, style='invis')
            dot.edge(str(node.key), inv_label, style="invis")
    
    return dot

def render_bst(bst):
    if bst.root == None:
        return
    dot = visualize_bst(bst)
    dot.attr(bgcolor="#1A1A1A")
    dot.render('bst_output', format='png', view=False)

class Button():
    def __init__(self, name, function=None):
        self.button = QPushButton(name)
        if function:
            self.button.clicked.connect(function)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.bst = bst()
        self.bst_reversed = False

        self.setWindowTitle("Binary Search Tree GUI")
        self.grid = QGridLayout(self)
        self.resize(900, 560)
        self.image_label = QLabel()
        self.text_label = QLabel()

        self.input_line = QLineEdit()
        valid = QIntValidator(0, 0x7fffffff, self)
        self.input_line.setValidator(valid)
    
        self.remove = Button("Remover", self.remover)
        self.insert = Button("Inserir", self.inserir)
        self.insert_lote = Button("Inserir em Lote", self.inserir_lote)
        self.reverse = Button("Inverter", self.inverter)
        self.clear = Button("Esvaziar", self.esvaziar)
        self.search = Button("Buscar", self.buscar)
        self.statistics = Button("Estatísticas", self.show_statistics)

        self.grid.addWidget(self.input_line, 0, 0)
        self.grid.addWidget(self.insert.button, 0, 1)
        self.grid.addWidget(self.search.button, 0, 2)
        self.grid.addWidget(self.remove.button, 0, 3)
        self.grid.addWidget(self.insert_lote.button, 1, 1)
        self.grid.addWidget(self.reverse.button, 1, 2)
        self.grid.addWidget(self.clear.button, 1, 3)
        self.grid.addWidget(self.image_label, 3, 0, Qt.AlignTop | Qt.AlignCenter)
        self.grid.addWidget(self.text_label, 3, 1, 1, 3, Qt.AlignTop | Qt.AlignLeft)
        self.grid.addWidget(QLabel("Amostra gráfica até o terceiro nível da árvore", alignment=Qt.AlignBottom), 4, 0, Qt.AlignBottom |Qt.AlignCenter)
        self.grid.addWidget(self.statistics.button, 4, 1, 1, 3, alignment=Qt.AlignCenter|Qt.AlignBottom)

        self.set_styles()

    def window_confirm(self, label):
        win = QDialog(self)
        layout = QVBoxLayout()
        label = QLabel(label)

        self.buttons = QDialogButtonBox()
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(win.accept)
        self.buttons.rejected.connect(win.reject)

        layout.addWidget(label)
        layout.addWidget(self.buttons)
        win.setLayout(layout)

        return win

    def show_bst(self):
        render_bst(self.bst)
        self.image_label.setPixmap(QPixmap('bst_output.png'))

    def show_dialog_window(self, text, icon):
        win = QDialog(self)
        win.setFixedSize(260, 160)
        win.setStyleSheet("background-color: #1A1A1A;")

        labl_icone = QLabel()
        icone = self.style().standardIcon(icon)

        label = QLabel()
        label.setText(text)

        labl_icone.setPixmap(icone.pixmap(40, 40))
        layout = QVBoxLayout()
        layout.addWidget(labl_icone, alignment=Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        win.setLayout(layout)

        win.exec()

    def show_statistics(self):
        if self.bst.root == None:
            win = self.show_dialog_window(
                "Árvore Vazia. Insira valores\npara ver estatísticas",
                self.style().StandardPixmap.SP_DialogCancelButton
            )
            return
        
        self.win = QDialog(self)
        self.win.setWindowTitle("Custo de Busca")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_statis)
        self.timer.start(500)

        show_graph = Button("Mostrar Aproximação Normal", self.show_normal_graph)
        self.statis_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.statis_label, alignment=Qt.AlignCenter)
        layout.addWidget(show_graph.button, alignment=Qt.AlignCenter)
        self.win.setLayout(layout)

        self.win.show()

    def show_normal_graph(self):
        if self.bst.root == None:
            return
        dq = Queue()
        dq.enqueue((self.bst.root, 0))
        x_list = []

        while not dq.empty():
            node, d = dq.dequeue()
            x_list.append(d)
            if node.left:
                dq.enqueue((node.left, d + 1))
            if node.right:
                dq.enqueue((node.right, d + 1))


        x = np.array(x_list)
        bins = np.arange(-0.5, max(x) + 1.5, 1.0)
        plt.hist(x, bins=bins, density=True, rwidth=1.0, color='skyblue', edgecolor='black')
        plt.xticks(sorted(list(set(x))))    
        plt.xlabel('Nível')
        plt.ylabel('Densidade de Nós')
        N = normal_dist(self.bst.average_cost(), np.sqrt(self.bst.variance()))
        N.plot_graph(-0.5, self.bst.height(self.bst.root) + 0.5)
        plt.show()
    
    def update_statis(self):
        if self.bst.root == None:
            self.win.done(0)
            return
        n = (self.bst.size(self.bst.root))
        h = np.floor(np.log2(n)) ##menor altura possivel numa BST
        ipl_min = (h - 2)*(2**(h)) + 2 ##calcula o ipl para h - 1 e soma s caminho pra chegar nele (h) 
        mean_min = ipl_min/n
        var_max = (n**2 - 1)/12
        ##pior caso : custo medio de busca numa lista encadeada (n + 1)/2
        self.statis_label.setText(
    f"""------------Média de Comparações-------
                    Melhor Caso: {round(mean_min + 1, 4)}
                    Caso Real: {round(self.bst.average_cost(), 4)}
                    Pior Caso: {(n + 1)/2} 

    ----------------Desvio Padrão---------------
                    Caso Real: {round(np.sqrt(self.bst.variance()), 4)}
                    Pior Caso: {round(np.sqrt(var_max), 4)}
    """
        )

    def inverter(self):
        if self.bst.root == None:
            self.image_label.setPixmap(QPixmap())
            return

        if not self.bst_reversed:
            self.bst.reverse(self.bst.root)
            self.show_bst()
            self.bst.reverse(self.bst.root)
        else:
            self.show_bst()

        self.bst_reversed = not self.bst_reversed

    def remover(self):
        num = self.input_line.text()
        if not num.strip():
            return
        self.set_descriptions()

        if self.bst.find(int(num)):
            win = self.window_confirm(f"Tem certeza que deseja remover o valor '{num}' da árvore?")
            if win.exec() == QDialog.DialogCode.Accepted:
                self.bst.remove(int(num))
        else:
            self.show_dialog_window(
                f"O valor '{num}' não foi encontrado.", 
                self.style().StandardPixmap.SP_DialogCancelButton
            )

        if self.bst.root == None:
            self.image_label.setPixmap(QPixmap())
            self.text_label.setText("")
            return
        self.show_bst()
        self.input_line.clear()
        self.set_descriptions()

    def esvaziar(self):
        if self.bst.root == None:
            win = QDialog(self)
            win.setFixedSize(240, 160)
            win.setStyleSheet("background-color: #1A1A1A;")

            label = QLabel("A árvore já está vazia!")
            layout = QVBoxLayout()
            layout.addWidget(label, alignment=Qt.AlignCenter)
            win.setLayout(layout)

            win.exec()
        else:
            win = self.window_confirm("Tem certeza que deseja esvaziar a árvore?")

            if win.exec() == QDialog.DialogCode.Accepted:
                self.bst.empty()
                self.image_label.setPixmap(QPixmap())

        self.set_descriptions()

    def inserir(self):
        num = self.input_line.text()
        if not num:
            return
        self.bst.put(int(num))

        self.show_bst()
        self.input_line.clear()
        self.set_descriptions()
    
    def inserir_lote(self):
        path = ""
        fdialog = QFileDialog(self)
        fdialog.setNameFilter("texto (*.txt)")
        fdialog.setOption(QFileDialog.DontUseNativeDialog)
        fdialog.setStyleSheet("background-color: #1A1A1A; color: white")

        if fdialog.exec_():
            path = fdialog.selectedFiles()[0]
        if not path:
            return

        with open(path) as f:
            toks = f.read().split('\n')

        for t in toks:
            if t.isdigit():
                self.bst.put(int(t))
                render_bst(self.bst)

        self.image_label.setPixmap(QPixmap('bst_output.png'))
        self.input_line.clear()
        self.set_descriptions()
            
    def buscar(self):
        num = self.input_line.text().strip()
        if not num:
            return
        win = QDialog(self)
        win.setFixedSize(240, 160)
        win.setStyleSheet("background-color: #1A1A1A;")
        
        nv = self.bst.depth(int(num), self.bst.root)

        print(nv)
        if nv < 0:
            self.show_dialog_window(
                f"O valor '{num}' não foi encontrado", 
                self.style().StandardPixmap.SP_DialogCancelButton
            )
        else:
            self.show_dialog_window(
                f"O valor '{num}' está na árvore.\nProfundidade: {nv}", 
                self.style().StandardPixmap.SP_DialogApplyButton
            )
        self.input_line.clear()

    def set_descriptions(self):
        if self.bst.root == None:
            self.text_label.setText("")
            return

        pre = self.bst.pre_order(self.bst.root).strip()
        pos = self.bst.pos_order(self.bst.root).strip()
        em = self.bst.in_order(self.bst.root).strip()
        level = self.bst.level_order().strip()
        n = self.bst.size(self.bst.root)

        _10_firsts = range(10 if n > 10 else n)
        more_than_10 = '...' if n > 10 else ''

        descriptions = f"""
            ---------------------DESCRIÇÕES-------------------

            Altura: {self.bst.height(self.bst.root)}
            Maior Valor: {self.bst.max()}
            Menor Valor: {self.bst.min()}
            Comprimento Interno: {self.bst.internalPathLength()}
            Tamanho (Número de chaves): {self.bst.size(self.bst.root)}
            Está Balanceado: {"Sim" if self.bst.is_balanced(self.bst.root) else "Não"}

            Pré-Ordem: {[int(pre.split()[i]) for i in _10_firsts]} {more_than_10}
            Em-Ordem: {[int(em.split()[i]) for i in _10_firsts]} {more_than_10}
            Pós-Ordem: {[int(pos.split()[i]) for i in _10_firsts]} {more_than_10}
            Em-Nível: {[int(level.split()[i]) for i in _10_firsts]} {more_than_10}
        """
        self.text_label.setText(descriptions)
        fwrite('pre_ordem.txt', pre)
        fwrite('pos_ordem.txt', pos)
        fwrite('em_ordem.txt', em)
        fwrite('em_nivel.txt', level)
        self.bst.pre_order(self.bst.root)

    def set_styles(self):
        self.insert.button.setStyleSheet("background-color: #240446; color: #ffffff")
        self.statistics.button.setStyleSheet("background-color: #240446")
        self.setStyleSheet("""
            QPushButton{
                background-color: #ff0000;
                color: #ffffff;
            } 
            QWidget{
                background-color: #1A1A1A;
            }
            QLineEdit{
                color: #ffffff;
                background-color: #111111;
            }
            QLabel{
                font-size: 16px;
                color: white;
            }
        """)