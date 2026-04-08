from pife import Pife
from interface import tela
from baralho import baralho

if __name__ == '__main__':

    while True:
        tela.Inicio()
            
        num_jogadores = tela.MenuIncluirJogadores()

        jogo = Pife(baralho)
        jogo.IncluirJogadores(num_jogadores)
        jogo.monte.embaralhar()
        jogo.DistribuirCartas()
        ##inicia o descarte com uma carta do monte
        jogo.descarte.moverCarta(jogo.monte)
        i = 0
        while True:
            jog_i = i

            tela.limpar()
            tela.Cabecalho()
            
            tela.PassaVez(jogo.jogadores[i])

            tela.ExibirStatusMesa(jogo, jogo.jogadores[i])

            tela.MostrarMao(jogo.jogadores[i])
            op = tela.Menu()
            if op == 1:
                jogo.PegaDoDescarte(jog_i)
            elif op == 2:
                jogo.PegaDoMonte(jog_i)

            if(len(jogo.monte.cartas) == 0):
                jogo.ReembaralhaMonte()

            if(jogo.jogadores[i].ContTrincas() >= 3):
                tela.MostrarVencedor(jogo.jogadores[i])
                input('pressione enter para voltar ao inicio...')
                break
            
            i = (i + 1) % num_jogadores