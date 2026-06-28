from collections import namedtuple 
from collections import deque 
from collections import ChainMap as _ChainMap
from collections import Counter as _Counter
from collections import OrderedDict as _OrderedDict
from collections import defaultdict


class NamedTuple: 
    def __init__(self):
        self.namedtuple_date = namedtuple('dates', ['value', 'hash'])
        self.namedtuple_set = []

    def put(self, value):
        self.namedtuple_set.append(self.namedtuple_date(value, hash(value)))

    def get(self, value):
        for e in self.namedtuple_set:
            if e.value == value:
                return value
        return False

    def delt(self, value):
        before = len(self.namedtuple_set)
        self.namedtuple_set = [e for e in self.namedtuple_set if e.value != value]
        return len(self.namedtuple_set) != before
    def print(self):
        return list(self.namedtuples_date.values())


class Deque:
    def __init__(self):
        self.deque_data = deque()

    def put(self, value):
        self.deque_data.append(value)

    def get(self, value):
        if value in self.deque_data:
            return value
        return False

    def delt(self, value):
        if self.get(value):
            self.deque_data.remove(value)
            return True
        return False

class ChainMap:
    def __init__(self):
        self.chainmap_data = _ChainMap({})

    def put(self, value):
        self.chainmap_data[value] = hash(value)

    def get(self, value):
        if value in self.chainmap_data:
            return value
        return False

    def delt(self, value):
        if value in self.chainmap_data:
            del self.chainmap_data[value]
            return True
        return False


class Counter:
    def __init__(self):
        self.counter_data = _Counter()

    def put(self, value):
        self.counter_data[value] += 1 

    def get(self, value):
        if self.counter_data[value] > 0:    
            return value
        return False

    def delt(self, value):
        if value in self.counter_data:
            del self.counter_data[value]
        return False


class OrderedDict:
    def __init__(self):
        self.ordereddict_data = _OrderedDict()

    def put(self, value):
        self.ordereddict_data[value] = hash(value)

    def get(self, value):
        if value in self.ordereddict_data:
            return value
        return False
    
    def delt(self, value):
        if self.get(value):
            del self.ordereddict_data[value]
            return True
        return False

class DefaultDict:
    def __init__(self):
        self.defaultdict_value = defaultdict(list)
    
    def put(self, value):
        self.defaultdict_value[value] = hash(value)

    def get(self, value):
        if value in self.defaultdict_value:
            return value
        return False
    
    def delt(self, value):
        if self.get(value):
            del self.defaultdict_value[value]
            return True
        return False