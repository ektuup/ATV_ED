import os
import sys

class Interface: ##classe para administrar informações do jogo na tela
    def Inicio(self):
        op = 0
        self.limpar()
        self.Cabecalho()

        print(f'{20*' '}Escolha uma opção:\n')
        print(f'{20*' '}1 - Iniciar partida')
        print(f'{20*' '}0 - Sair')
        while True:
            try:
                op = int(input())
                if(op == 1 or op == 0):
                    break
            except:
                print('Erro: estão disponíveis apenas as opções 1 e 0')
        self.limpar()
        if op == 0:
            sys.exit()

    def Cabecalho(self):
        print(f'{30*'-'}PIFE{30*'-'}')

    def limpar(self):
        if os.name == 'nt': ##se for windows, usa comando do windows
            os.system('cls')
        else:
            os.system('clear')

    def MenuIncluirJogadores(self):
        while True:
            try:
                num = int(input('Quantas pessoas vão jogar? (máximo 4 e mínimo 2): '))
                if num >= 2 and num <= 4:
                    break
            except ValueError:
                self.limpar()
                self.Cabecalho()
                print('Erro: A quantidade de pessoas deve ser um numero inteiro de 2 a 4. tente novamente')
        return num
    
    def Menu(self):
        while True: 
            print('''-----------Escolha uma opção--------------
            1 - Comprar do Descarte
            2 - Comprar do Monte
            ''')
            while True:
                try:
                    op = int(input())
                    if 1 == op or op == 2:
                        return op
                    print('informe uma opção válida (1 ou 2)')
                except:
                    print('informe uma opção válida (1 ou 2)')




    
    def PassaVez(self, jog_i): ##essa função serve para avisar de quem é a vez sem mostrar suas cartas
        input(f"vez de '{jog_i.nome}' (pressione enter para ver suas cartas...)")
        self.limpar()
        self.Cabecalho()

    def ExibirStatusMesa(self, jogo, jogador):
        print(f"vez de '-----{jogador.nome}-----'")
        print(f"topo Descarte: {jogo.descarte.topo()}\n")

    def MostrarMao(self, jogador):
        print('Sua Mão: \n ', end = '')

        for i in range(len(jogador.cartas)): ##mostra as posições das cartas na mão
            print(f'({i + 1})  ', end='')

        print()

        for i in range(len(jogador.cartas)):
            print(f'{jogador.cartas[i]} ', end='') 
        print('\n')

    def MostrarVencedor(self, jogador):
        print(30*'-')
        print('PARABÉNS!')
        print(f"jogador '{jogador.nome}' ganhou a partida")
        print(30*'-')
        print('TRINCAS:')
        for t in jogador.trincas:
            for carta in t:
                print(f"{carta}", end = '  ')
            print()

tela = Interface()