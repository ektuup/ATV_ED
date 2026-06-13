import graphviz
from BST import bst
from my_queue import Queue

import graphviz

def visualize_bst(bst, dot=None):
    if dot == None:
        dot = graphviz.Digraph()
    
    dq = Queue()
    dq.enqueue((bst.root, 0))

    while not dq.empty():
        node = dq.dequeue()

        dot.node(str(node.key), shape='circle')
        
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            dq.enqueue(node.left)
        elif node.right:
            inv_label = f"lbl_{node.key}"
            dot.node(inv_label, style='invis')
            dot.edge(str(node.key), inv_label, style="invis")
        
        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            dq.enqueue(node.right)
        elif node.right:
            inv_label = f"lbl_{node.key}"
            dot.node(inv_label, style='invis')
            dot.edge(str(node.key), inv_label, style="invis")
    
    return dot

def visualize_bst(node, dot=None):
    if dot is None:
        dot = graphviz.Digraph()
        dot.attr(ordering="out") 

    if node:
        dot.node(str(node.key), shape="circle")
        
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            visualize_bst(node.left, dot)
        elif node.right:
            inv_label = f"inv_l_{node.key}"
            dot.node(inv_label, style="invis", width="0.1", height="0.1", label="")
            dot.edge(str(node.key), inv_label, style="invis")

        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            visualize_bst(node.right, dot)

        elif node.left:
            inv_label = f"inv_r_{node.key}"
            dot.node(inv_label, style="invis", width="0.1", height="0.1", label="")
            dot.edge(str(node.key), inv_label, style="invis")

    return dot


bst = bst()
bst.put(10)
bst.put(-1)
bst.put(1)

arvore_dot = visualize_bst(bst.root)
arvore_dot.attr(size='12,12')
# arvore_dot.attr(ratio='fill')
arvore_dot.render('bst_output', format='png', view=True)
