import os
from jogador import Jogador
from baralho import Baralho
from interface import tela

class Pife:
    def __init__(self, baralho):
        self.monte = baralho #monte de compra
        self.descarte = Baralho() #lixo ou descarte
        self.jogadores = []

    def DistribuirCartas(self):
        for j in self.jogadores:
            for i in range(9):
                c = j.comprarCarta(self.monte) #distribui 9 cartas pra cada jogador
            j.ordenaMao()

    def IncluirJogadores(self, num_jogadores):
        self.num_jogadores = num_jogadores

        for i in range(self.num_jogadores):
            nome = input(f'Nome do jogador {i + 1}: ')
            jog = Jogador(nome)
            self.jogadores.append(jog)
    
    def PegaDoDescarte(self, jog_i):
        self.jogadores[jog_i].comprarCarta(self.descarte) #faz o jogador jog_i comprar do descarte

        while True:
            try:
                ind = int(input('Carta que você vai descartar: '))

                if ind > 0:
                    self.jogadores[jog_i].descartarCarta(ind - 1, self.descarte) #descarta primeiro e só depois ordena a mao para evitar erro de indice 
                    self.jogadores[jog_i].ordenaMao()
                    return
                else:
                    print('Erro: informe a posição da carta (numero de 1 a 9)') #erro na conversao pra int, ex: usuario digitou 'ola'
            except:
                print('Erro: informe a posição da carta (numero de 1 a 9)') #erro na conversao pra int, ex: usuario digitou 'ola'

    def PegaDoMonte(self, jog_i):
        self.jogadores[jog_i].comprarCarta(self.monte)
        self.jogadores[jog_i].ordenaMao()
        
        tela.limpar()
        tela.Cabecalho()
        
        tela.ExibirStatusMesa(self, self.jogadores[jog_i])
        tela.MostrarMao(self.jogadores[jog_i])
        while True:
            try:
                ind = int(input('Carta que você vai descartar: '))

                if ind > 0:
                    self.jogadores[jog_i].descartarCarta(ind - 1, self.descarte)
                    return
                else:
                    print(f'Erro: informe a posição da carta (numero de 1 a {len(self.jogadores[jog_i].cartas)})')
            except:
                print(f'Erro: informe a posição da carta (numero de 1 a {len(self.jogadores[jog_i].cartas)})')


    def ReembaralhaMonte(self): 
    ##em algum momento o monte pode acabar, esse método pega tudo o que estava no descarte e devolve pro monte, exceto a carta do topo
        topo = self.descarte.cartas.pop()
        self.monte.juntaBaralho(self.descarte)
        self.monte.embaralhar()

        self.descarte.cartas.clear()
        self.descarte.cartas.append(topo)
