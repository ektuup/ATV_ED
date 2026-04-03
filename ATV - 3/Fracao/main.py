import os
from fraction import fraction
from fraction import gcd

def limpa_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def Menu():
    print(f'''{20*'-'}CALCULADORA-DE-FRAÇÃO{20*'-'}
              Escolha uma opção:
                1 - Somar
                2 - Subtrair
                3 - Multiplicar
                4 - Dividir
                5 - Comparar
                0 - Sair
            ''')
    while True:
        try:
            op = int(input())
            if 0 <= op <= 5:
                break
            print('informe uma opção válida (numero de 0 a 5)')    
        except:
            print('informe uma opção válida (numero de 0 a 5)')    
    return op
            



if __name__ == '__main__':
    while True:
        op = Menu()
        limpa_tela()

        if op == 0:
            break

        f1 = fraction.read('informe a primeira fração: ')
        f2 = fraction.read('informe a segunda fração: ')
        
        match op:
            case 1:
                print(f'({f1}) + ({f2}) = {f1 + f2}')
            case 2:
                print(f'({f1}) - ({f2}) = {f1 - f2}')
            case 3:
                print(f'({f1})*({f2}) = {f1 * f2}')
            case 4:
                if f2.getNum() == 0:
                    print('Divisão por 0 não é permitida')
                else:
                    print(f'({f1})/({f2}) = {f1 / f2}')
            case 5:
                if f1 == f2:
                    print('iguais')
                elif f1 != f2:
                    print('diferentes')
                
                if f1 > f2:
                    print(f'{f1} > {f2}')
                elif f1 < f2:
                    print(f'{f1} < {f2}')
            
        
    

