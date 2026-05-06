import time
import os
import csv

class Array:
    def __init__(self, size = 64):
        self.size = size
        self.array = [None] * self.size
        self.len = 0

    def insert(self, value):
        self.realoc()

        self.array[self.len] = value
        self.len += 1

    def realoc(self):
        prop = self.len/self.size

        if prop > 0.8:
            self.size *= 2
            array_aux = [None] * self.size

            for i in range(self.len):
                array_aux[i] = self.array[i]

            self.array = array_aux

    def copy(self):
        temp = Array()
        for i in range(self.len):
            temp.insert(self.array[i])

        return temp
        
        
class FileSort:
    def __init__(self, path):
        self.arr = Array()
        self.arr_sorted  = Array()
        self.file = path
        self.ord_file = os.path.dirname(path) + "/ordened_" + os.path.basename(path)
        self.time = 0
        self.trades = 0

    def FileReading(self):
        with open(self.file, 'r', encoding='utf-8') as tx:
            for line in tx:
                line = line.strip()
                self.arr.insert(line)
    
    def InsertionSort(self):
        self.trades = 0
        start = time.perf_counter()

        self.arr_sorted = self.arr.copy()
        for i in range(1, self.arr_sorted.len):
            current = self.arr_sorted.array[i]
            j = i - 1

            while j >= 0 and self.arr_sorted.array[j] > current:
                self.trades += 1
                self.arr_sorted.array[j + 1] = self.arr_sorted.array[j] 
                j -= 1

            self.arr_sorted.array[j + 1] = current

        end = time.perf_counter()
        self.time = end - start

    def OrdenedFileWrite(self):
        with open(self.ord_file, 'w', encoding = 'utf-8') as tx:
            for i in range(self.arr_sorted.len):
                tx.write(f"{self.arr_sorted.array[i]}\n")

        file_exist = os.path.isfile('sorting_statistics.csv')

        with open('sorting_statistics.csv', 'a') as ftimes:
            writer = csv.writer(ftimes)
            if not file_exist:
                writer.writerow(["Tempo_de_ordenacao", "Numero_de_elementos", "Quantidade_de_trocas"])

            writer.writerow([self.time, self.arr.len, self.trades])

    def getTime(self):
        return self.time

    def getTrades(self):
        return self.trades

    def getElements(self):
        return self.arr.len
