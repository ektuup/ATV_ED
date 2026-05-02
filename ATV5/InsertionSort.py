import time

class Array:
    def __init__(self, size = 5):
        self.size = size
        self.array = [None] * self.size
        self.index = 0

    def insert(self, value):
        self.realoc()

        self.array[self.index] = value
        self.index += 1

    def realoc(self):
        prop = self.index/self.size

        if prop > 0.8:
            self.size *= 2
            array_aux = [None] * self.size

            for i in range(self.index):
                array_aux[i] = self.array[i]

            self.array = array_aux
        
class FileSort:
    def __init__(self, file):
        self.arr = Array()
        self.file = file
        self.ord_file = "ordened_" + file
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

        for i in range(1, self.arr.index):
            current = self.arr.array[i]
            j = i - 1

            while j >= 0 and self.arr.array[j] > current:
                self.trades += 1
                self.arr.array[j + 1] = self.arr.array[j] 
                j -= 1

            self.arr.array[j + 1] = current
        end = time.perf_counter()
        self.time = end - start

    def OrdenedFile(self):
        with open(self.ord_file, 'w', encoding = 'utf-8') as tx:
            for i in range(self.arr.index):
                tx.write(self.arr.array[i] + "\n")

    def getTime(self):
        return self.time

    def getTrades(self):
        return self.trades

    def getElements(self):
        return self.arr.index
