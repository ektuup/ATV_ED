from tkinter import *
from tkinter import filedialog, ttk
import os
from InsertionSort import FileSort

class GUI:
    def __init__(self, window):
        self.window = window
        self.file = None
        self.time_sort = None
        
        window.config(bg = "#FFEDCE")
        window.geometry("840x640")

        self.status = Label(self.window, bg = "#FFEDCE", text="")
        self.status.pack(side = TOP)

        self.monitor = Text(self.window,
                            width = 60, 
                            height = 15,
                            relief= "solid",
                            bg = "#FFC193",
                            fg = '#FF3737',
                            font = ("Arial", 12),
                            padx = 20,
                            pady = 20)
        self.monitor.config(state = "disabled")
        self.monitor.pack(pady = 85, side = BOTTOM)

        frame = Frame(bg = '#FFEDCE', bd = 10)
        
        Button(frame, bg = '#FF8383', activebackground = '#FF3737', 
               text = "Carregar arquivo", command = self.chooseFile).pack(side = TOP)
        Button(frame, bg = '#FF8383', activebackground = '#FF3737',
               text = "Ordenar e salvar arquivo ordenado", command = self.Sort).pack(side = TOP)    
        Button(frame, bg = '#FF8383', activebackground = '#FF3737',
               text = "Listar 10 primeiros sem ordenação", command = self.displayDisordered).pack(side = LEFT)
        Button(frame, bg = '#FF8383', activebackground = '#FF3737',
               text = "Listar 10 primeiros ordenados", command = self.displayOrdered).pack(side = LEFT)
        Button(frame, bg = '#FF8383', activebackground = '#FF3737',
               text = "Exibir estatísticas sobre a ordenação", command = self.sortStats).pack(side = LEFT)

        frame.pack(side = TOP)

    def Sort(self):
        self.status.config(text="Ordenando...")
        self.window.update_idletasks()

        self.file.InsertionSort()
        self.time_sort = self.file.getTime()

        self.status.config(text="Concluído!")

        self.file.OrdenedFile()

    def chooseFile(self):
        path = filedialog.askopenfilename()
        filename = os.path.basename(path)
        self.file = FileSort(filename)

        self.file.FileReading()

    def displayDisordered(self):
        self.status.config(text="")
        self.monitor.config(state = "normal")
        self.monitor.delete("1.0", END)
        with open(self.file.file, 'r', encoding = 'utf-8') as tx:
            linha = tx.readline()
            for i in range(10):
                self.monitor.insert(END + "\n", linha)
                linha = tx.readline()
        self.monitor.config(state = "disabled")

    def displayOrdered(self):
        self.status.config(text="")
        self.monitor.config(state = "normal")
        self.monitor.delete("1.0", END)
        with open(self.file.ord_file, 'r', encoding = 'utf-8') as tx:
            linha = tx.readline()
            for i in range(10):
                self.monitor.insert(END + "\n", linha)
                linha = tx.readline()

        self.monitor.config(state = "disabled")

    def sortStats(self):
        self.status.config(text="")
        self.monitor.config(state = "normal")
        self.monitor.delete('1.0', END)
        self.monitor.insert(END, f"Tempo de ordenação: {self.time_sort:.10f} segundos\n") 
        self.monitor.insert(END, f"Quantidade de trocas: {self.file.getTrades()}\n") 
        self.monitor.insert(END, f"Quantidade de elementos: {self.file.getElements()}")
        self.monitor.config(state = "disabled")

window = Tk()
GUI(window)
window.mainloop()
