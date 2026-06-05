from queue import Queue

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    #privados:
    def _pre_order(self, root):
        if(root == None): 
            return
        
        print(root.key)
        self._pre_order(root.left)
        self._pre_order(root.right)

    def _in_order(self, root):
        if(root == None):
            return        
        self._in_order(root.left)
        print(root.key)
        self._in_order(root.right)
    
    def _pos_order(self, root):
        if(root == None):
            return
        
        self._pos_order(root.left)
        print(root.key)
        self._pos_order(root.right)

    def _size(self, root):
        if(root == None): 
            return 0
        return self._size(root.left) + self._size(root.right) + 1
    
    def _is_balanced(self, root):
        if(root == None):
            return True
         
        esq = self._is_balanced(root.left)
        dirt = self._is_balanced(root.right)
        
        if not (esq and dirt):
            return False

        if(abs(self.fb(root)) > 1):
            return False
        return True   

    #Publicos

    def put(self, key):
        new = Node(key)
        if(self.root == None):
            self.root = new
            return
        
        aux = self.root
        prev = None
        while aux:
            prev = aux
            if(key == aux.key):
                return
            
            if(key < aux.key):
                aux = aux.left
            else:
                aux = aux.right
            
        if key < prev.key:
            prev.left = new
        else:
            prev.right = new

    def find(self, key):
        aux = self.root

        while aux:
            if key == aux.key:
                return True
            elif key < aux.key:       
                aux = aux.left
            else:
                aux = aux.right
        return False

    def pos_order(self):
        self._pos_order(self.root)

    def pre_order(self):
        self._pre_order(self.root)

    def in_order(self):
        self._in_order(self.root)

    def level_order(self):
        if self.root == None:
            return
    
        dq = Queue()
        dq.enqueue(self.root)

        while not dq.empty():
            aux = dq.dequeue()
            print(aux.key)

            if aux.left:
                dq.enqueue(aux.left)
            if aux.right:
                dq.enqueue(aux.right)   

    def min(self):
        if self.root == None:
            return None

        aux = self.root
        while aux.left:
            aux = aux.left
        return aux.key

    def max(self):
        if self.root == None:
            return None
        
        aux = self.root
        while aux.right:
            aux = aux.right
        return aux.key

    def empty(self):
        self.root = None
    
    def size(self):
        return self._size(self.root)

    def height(self, root):
        if root == None:
            return -1
        return max(self.height(root.left), self.height(root.right)) + 1

    def depth(self, key, root):
        if root == None:
            return -1
        if root.key == key:
            return 0
        
        deep_left = self.depth(key, root.left)
        deep_right = self.depth(key, root.right)
        
        if deep_left != -1:
            return deep_left + 1
        elif deep_right != -1:
            return deep_right + 1

        return -1

    def fb(self, root):
        if root == None:
            return 0
        return self.height(root.left) - self.height(root.right)

    def is_balanced(self):
        return self._is_balanced(self.root)
    
    def internal_path_length(self):
        dq = Queue()
        dq.enqueue((self.root, 0))
        cont = 0
    
        while not dq.empty():
            aux, d = dq.dequeue()
            cont += d
            
            if aux.left:
                dq.enqueue((aux.left, d + 1))
            if aux.right:
                dq.enqueue((aux.right, d + 1))
        return cont

                
if __name__ == '__main__':
    bt = BST()
    bt.put(2)
    bt.put(7)
    bt.put(3)
    bt.put(12)
    bt.put(17)
    bt.put(0)
    bt.put(23)

    print(bt.height(bt.root))
    print(bt.depth(12, bt.root))
    print(bt.is_balanced())
    print(bt.internal_path_length())
    print(bt.size())
    print(bt.max())
    print(bt.min())
    print(bt.find(3))
    print(bt.find(18))



