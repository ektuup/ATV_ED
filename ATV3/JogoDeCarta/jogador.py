class Jogador:
    def __init__(self, nome):
        global baralho
        self.nome = nome
        self.cartas = [] ##mão do jogador
        self.trincas = [[]]

    def __str__(self):
        texto =  f"{self.nome} : "
        for c in self.cartas:
            texto += c.__str__() + ';'
        return texto

    def descartarCarta(self, ind, BaralDest):
        c = self.cartas.pop(ind)
        BaralDest.cartas.append(c)
        return c

    def comprarCarta(self, origem):
        c = origem.cartas.pop()
        self.cartas.append(c)
        return c

    def ordenaMao(self):
        self.cartas.sort()

    def ContTrincas(self):
        self.trincas = []
        trinca = [self.cartas[0]]
        
        for i in range(len(self.cartas) - 1):
            atual = self.cartas[i]
            prox = self.cartas[i + 1]

            if atual.num == prox.num and len(trinca) < 3:
                trinca.append(prox)
            else:
                if len(trinca) == 3:
                    self.trincas.append(trinca)
                trinca = [prox]
        
        if len(trinca) == 3:
            self.trincas.append(trinca)
        return len(self.trincas)
