from tkinter import *
from tkinter import filedialog, ttk
import os
import csv
from InsertionSort import FileSort

class GUI:
    def __init__(self, window):
        self.window = window
        self.file = None
        self.avegare_time_sort = 0
        self.num_of_sorts = 0
        window.config(bg = "#222220")   
        window.geometry("840x640")
        window.resizable(False, False)

        self.status = Label(self.window, bg = "#222220", fg = "#FFFFFF",text="")
        self.status.pack(side = TOP)

        self.monitor = Text(self.window,
                            width = 60, 
                            height = 15,
                            relief= "solid",
                            bg = "#3A3A39",
                            fg = '#FFFFFF',
                            font = ("Arial", 12),
                            padx = 20,
                            pady = 20)

        self.monitor.config(state = "disabled")
        self.monitor.pack(pady = 85, side = BOTTOM)

        frame = Frame(bg = "#3A3A39", bd = 10)
        
        Button(frame, bg = "#9646CF", activebackground = '#FF3737', 
               text = "Carregar arquivo", command = self.chooseFile).pack(side = TOP)
        Button(frame, bg = '#9646CF', activebackground = '#FF3737',
               text = "Ordenar e salvar arquivo ordenado", command = self.Sort).pack(side = TOP)    
        Button(frame, bg = '#9646CF', activebackground = '#FF3737',
               text = "Listar 10 primeiros sem ordenação", command = self.displayDisordered).pack(side = LEFT)
        Button(frame, bg = '#9646CF', activebackground = '#FF3737',
               text = "Listar 10 primeiros ordenados", command = self.displayOrdered).pack(side = LEFT)
        Button(frame, bg = '#9646CF', activebackground = '#FF3737',
               text = "Exibir estatísticas sobre a ordenação", command = self.sortStats).pack(side = LEFT)

        frame.pack(side = TOP)

    def Sort(self):
        self.status.config(text="")
        self.monitor.config(state = "normal")
        self.monitor.delete("1.0", END)
        
        try:
            if self.file is None:
                raise Exception

            self.status.config(text="Ordenando...")
            self.window.update_idletasks()

            self.file.InsertionSort()

            self.status.config(text="Concluído!")

            self.file.OrdenedFileWrite()
        except Exception as e:
            self.monitor.delete("1.0", END)
            self.monitor.config(state = 'normal')
            self.monitor.insert(END, f"Ação inválida: Selecione um arquivo; {e}\n")
            self.monitor.config(state = "disable")


    def chooseFile(self):
        try:
            self.status.config(text="")
            self.monitor.config(state = "normal")
            self.monitor.delete("1.0", END)
            path = filedialog.askopenfilename()
            self.file = FileSort(path)
            self.status.config(text=self.file.ord_file)
            self.file.FileReading()
        except:
            self.monitor.delete("1.0", END)
            self.monitor.config(state = 'normal')
            self.monitor.insert(END, "Ação inválida.\n")
            self.monitor.config(state = "disable")
        

    def displayDisordered(self):
        try:
            self.status.config(text="")
            self.monitor.config(state = "normal")
            self.monitor.delete("1.0", END)

            for i in range(10):
                self.monitor.insert(END + "\n", self.file.arr.array[i] + '\n')

            self.monitor.config(state = "disabled")
        except:
            self.monitor.delete("1.0", END)
            self.monitor.config(state = 'normal')
            self.monitor.insert(END, "Ação inválida: Selecione um arquivo\n")
            self.monitor.config(state = "disable")
        

    def displayOrdered(self):
        try:
            self.status.config(text="")
            self.monitor.config(state = "normal")
            self.monitor.delete("1.0", END)

            for i in range(10):
                self.monitor.insert(END + "\n", self.file.arr_sorted.array[i] + '\n')

            self.monitor.config(state = "disabled")
        except:
            self.monitor.delete("1.0", END)
            self.monitor.config(state = 'normal')
            self.monitor.insert(END, "Ação inválida: Selecione e ordene um arquivo\n")
            self.monitor.config(state = "disable")

    def sortStats(self):
        self.status.config(text="")
        self.monitor.config(state = "normal")
        self.monitor.delete("1.0", END)
        
        try:
            if self.file is None:
                raise Exception
            time, elements, trades = self.getAverage()


            self.monitor.insert(END, f"Tempo médio de ordenação: {time:.10f} segundos\n") 
            self.monitor.insert(END, f"Quantidade média de elementos: {elements}\n")
            self.monitor.insert(END, f"Quantidade média de trocas: {trades}\n") 
            self.monitor.insert(END, f"Quantidade de ordenações: {self.getNumOfSorts()}\n") 
            self.monitor.config(state = "disabled")
        except Exception as e:
            self.monitor.delete("1.0", END)
            self.monitor.config(state = 'normal')
            self.monitor.insert(END, f"Ação inválida: Selecione e ordene um arquivo {e}\n" )
            self.monitor.config(state = "disable")

    def getAverage(self):
        sum_time = 0.0
        sum_elements = 0
        sum_trades = 0
        cont = 0
        with open('sorting_statistics.csv', 'r') as ftimes:
            reader = csv.reader(ftimes)

            for line in reader:
                if line and line[0] == "Tempo_de_ordenacao":
                    continue

                if len(line) == 3:
                    sum_time += float(line[0])
                    sum_elements += int(line[1])
                    sum_trades += int(line[2])
                    cont += 1 
        return sum_time/cont, sum_elements/cont, sum_trades/cont
    
    def getNumOfSorts(self):
        cont = 0
        with open('sorting_statistics.csv', 'r') as ftimes:
            reader = csv.reader(ftimes)

            for line in reader:
                cont += 1;
        
        return cont - 1; ##remove o reader


if __name__ == '__main__':
    window = Tk(className=" Estatisticas Insertion Sort")
    GUI(window)
    window.mainloop()
