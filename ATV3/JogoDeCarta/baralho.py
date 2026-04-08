import random
from carta import Carta

class Baralho:
    def __init__(self, numeros = None, naipes = None):
        self.cartas = []
        if numeros == None and naipes == None:
            return
        for i in numeros: 
            for j in naipes:
                self.cartas.append(Carta(i, j)) ##faz um produto cartesiano para gerar todas as cartas possiveis com naipe e numero

    def __str__(self):
        texto = ""
        for c in self.cartas[::-1]:
            texto += c.__str__() + '\n'
        return texto
        
    def topo(self):
        return self.cartas[-1]
    
    def embaralhar(self):
        random.shuffle(self.cartas) ##shuffle cria uma permutação aleatória in-place
    
    ##move a carta do baralho origem para o self
    def moverCarta(self, BaralOrigem):
        self.cartas.append((BaralOrigem.cartas.pop()))

    def juntaBaralho(self, baral2): #move o baral2 todo para o baralho self
        self.cartas.extend(baral2.cartas)

naipes = ["♥", "♦", "♠", "♣"]
numeros = range(1, 14)
baralho = Baralho(numeros, naipes)