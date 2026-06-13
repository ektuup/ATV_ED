from my_queue import Queue

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class bst:
    def __init__(self):
        self.root = None

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

            aux = aux.left if key < aux.key else aux.right            
            
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

    def in_order(self, root):
        if(root == None):
            return ""

        s = self.in_order(root.left)
        s += str(root.key) + " "  
        s += self.in_order(root.right)
        return s


    def pos_order(self, root):
        if(root == None):
            return ""

        s = self.pos_order(root.left)
        s += self.pos_order(root.right)
        s += str(root.key) + " "  
        return s 


    def pre_order(self, root):
        if(root == None):
            return ""

        s = str(root.key) + " " 
        s += self.pre_order(root.left)
        s += self.pre_order(root.right)
        
        return s

    def level_order(self):
        if self.root == None:
            return ""
        s = ""
        dq = Queue()
        dq.enqueue(self.root)

        while not dq.empty():
            aux = dq.dequeue()
            s += f"{aux.key} "

            if aux.left:
                dq.enqueue(aux.left)
            if aux.right:
                dq.enqueue(aux.right)

        return s.strip()
            
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
    
    def size(self, root):
        if(root == None): 
            return 0
        return self.size(root.left) + self.size(root.right) + 1

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

    def is_balanced(self, root):
        if(root == None):
            return True
         
        esq = self.is_balanced(root.left)
        dirt = self.is_balanced(root.right)
        
        if not (esq and dirt):
            return False

        if(abs(self.fb(root)) > 1):
            return False
        return True    
    
    def internalPathLength(self):
        if self.root == None:
            return
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

    def remove_root(self, root):
        if root == None:
            return
        if root.left == None:
            q = root.right
            return q
        
        p = root
        q = p.left

        while q.right:
            p = q
            q = q.right

        if p != root:
            p.right = q.left
            q.left = root.left

        q.right = root.right
        return q

    def remove(self, key):
        if self.root == None:
            return
        if self.root.key == key:
            self.root = self.remove_root(self.root)
            return

        aux = self.root
        p = None
        while aux:
            if key == aux.key:
                break
            p = aux
            aux = aux.left if key < aux.key else aux.right
            
        if p == None:
            return

        if p.left and p.left.key == key:
            p.left = self.remove_root(p.left)
        else: 
            p.right = self.remove_root(p.right)
   
    def reverse(self, root):
        if root == None:
            return

        self.reverse(root.left)
        self.reverse(root.right)
        
        t = root.left
        root.left = root.right
        root.right = t    




