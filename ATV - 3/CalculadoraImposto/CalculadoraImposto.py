import os

class Contribuinte:

    def __init__(self, nome):
        self.nome = nome
        self.salario = 0
        self.imposto = 0
        self.deducao = 0

    def calculadoraAliquota(self, faixa):
        tabela_imposto = [0, 0.075, 0.05] 
        imposto_faixa = self.salario * tabela_imposto[faixa]
        self.imposto += imposto_faixa

    def calculadoraDeducao(self, faixa):
        tabela_deducao = [0, 158.4, 381.44, 662.77, 896]
        self.salario += tabela_deducao[faixa]
        self.deducao = tabela_deducao[faixa]

    def calculadoraTotal(self):
        flag_deducao = 0
        if self.salario <= 2259.20:
            self.calculadoraAliquota(0)

        if self.salario >= 2259.21:
            self.calculadoraAliquota(1)
            flag_deducao += 1
        if self.salario >= 2826.66:
            self.calculadoraAliquota(1)
            flag_deducao += 1
        if self.salario >= 3751.06:
            self.calculadoraAliquota(1)
            flag_deducao += 1
        if self.salario >= 4664.69:
            self.calculadoraAliquota(2)
            flag_deducao += 1

        self.salario -= self.imposto 
        self.calculadoraDeducao(flag_deducao)

def limpatela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    limpatela()
    print("---------------------------------------------------")
    print("Olá, Boas vindas à calculadora de imposto de renda!")
    print("---------------------------------------------------")
    print()
    menuImposto()
    while True:
        print()
        print("Você deseja calcular o imposto de outro contribuinte?")
        try:
            op = int(input("1 - SIM\n2 - NÃO\n"))
            match op:
                case 1:
                    limpatela()
                    menuImposto()
                case 2:
                    limpatela()
                    print("Até logo!\nFim do programa...")
                    break
                case _:
                    limpa()
                    print("Opção indisponível!")
        except:
            limpatela()
            print("Erro!\nDigite uma opção válida!")


def menuImposto():
    usuario = Contribuinte(input("Como devemos te chamar? "))
    while True:
        try:
            usuario.salario = salario_antes = float(input(f"{usuario.nome}, informe o seu salário mensal: "))
            break
        except:
            limpatela()
            print(f"Erro!\n{usuario.nome}, por favor, digite apenas o valor de seu salário.")

    usuario.calculadoraTotal()
    
    limpatela()
    print(f"Imposto calculado, {usuario.nome}!")
    print()
    print(f"Impostos totais: {usuario.imposto}")
    print(f"Dedução do impostos: {usuario.deducao}")
    print()
    print(f"Salário antes dos descontos: {salario_antes}")
    print(f"Sálario após descontos: {usuario.salario}")

if __name__ == "__main__":
    menu()
