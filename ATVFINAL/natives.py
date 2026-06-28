class Dict:
    def __init__(self):
        self.dict_data = {}

    def put(self, value):
        self.dict_data[value] = hash(value)

    def get(self, value):
        if value in self.dict_data:
            return value
        return False
    def delt(self, value):
        self.dict_data.pop(value)

class List:
    def __init__(self):
        self.list_data = []

    def put(self, value):
        self.list_data.append(value)

    def get(self, value):
        if value in self.list_data:
            return value
        return False

    def delt(self, value):
        if self.get(value):
            self.list_data.remove(value)
            return True
        return False

class Set:
    def __init__(self):
        self.set_data = set()

    def put(self, value):
        self.set_data.add(value)
    
    def get(self, value):
        if value in self.set_data:
            return value
        return False

    def delt(self, value):
        if self.get(value):
            self.set_data.remove(value)
            return True
        return False

class Tuple:
    def __init__(self):
        self.buf = []
        self.tuple_data = ()

    def put(self, value):
        self.buf.append(value)

    def flush(self):
        if self.buf:
            self.tuple_data = (*self.tuple_data, *self.buf)
            self.buf = []

    def get(self, value):
        self.flush()
        return value if value in self.tuple_data else False

    def delt(self, value):
        self.flush()
        before = len(self.tuple_data)
        self.tuple_data = tuple(x for x in self.tuple_data if x != value)
        return len(self.tuple_data) != before
