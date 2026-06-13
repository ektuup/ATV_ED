class node:
    def __init__(self, value):
        self.data = value
        self.next = None
    
class Queue:
    def __init__(self):
        self.front = None
        self.tail = None
    
    def enqueue(self, value):
        new = node(value)
        if(self.front == None):
            self.front = new
            self.tail = new
            return
        
        self.tail.next = new
        self.tail = new
    
    def dequeue(self):
        if self.empty():
            return 
        value = self.front.data
        self.front = self.front.next

        return value
    
    def show(self):
        aux = self.front
        while aux:
            print(f"{aux.data} -> ", end='')
            aux = aux.next
        print()
    
    def empty(self):
        return self.front == None
    
